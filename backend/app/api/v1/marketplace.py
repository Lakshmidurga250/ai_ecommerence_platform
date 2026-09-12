"""
Marketplace & Order Orchestration API Router.
Exposes multi-vendor seller scorecards, automated order splitting,
return eligibility evaluations, and context-grounded AI support assistant.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict

from app.core.database import get_db
from app.dependencies.auth import get_current_active_user, get_current_admin_user
from app.dependencies.tenant import get_current_seller
from app.models.user import User
from app.models.seller import Seller
from app.services.marketplace_service import MarketplaceService
from app.services.order_orchestration_service import OrderOrchestrationService
from app.services.ai_support_service import AISupportService
from ai.pricing.dynamic_pricing_engine import DynamicPricingEngine


router = APIRouter(prefix="/marketplace", tags=["Marketplace & Order Orchestration"])


# Schemas
class PayoutCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: float = Field(..., gt=0, description="Payout withdrawal amount")
    notes: Optional[str] = Field(None, description="Optional vendor notes")


class PayoutActionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    action: str = Field(..., description="Action: APPROVE, COMPLETE, or REJECT")
    reference: Optional[str] = Field(None, description="External banking wire/transfer reference")


class ItemStatusUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str = Field(..., description="Updated item status e.g. SHIPPED, DELIVERED, CANCELLED")


class SupportChatRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str = Field(..., min_length=1, description="Customer inquiry message")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Session context")


# Endpoints

@router.get("/scorecard")
def get_my_seller_scorecard(
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db)
):
    """Retrieves live fulfillment rates, customer ratings, and net payable balances for the authenticated seller."""
    return MarketplaceService.get_seller_scorecard(db, seller.id)


@router.post("/payouts/request")
def request_seller_payout(
    data: PayoutCreateSchema,
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db)
):
    """Submits a payout withdrawal against the seller's available balance."""
    payout = MarketplaceService.request_payout(db, seller.id, data.amount, data.notes)
    return {
        "status": "success",
        "message": f"Payout request of ${data.amount:.2f} submitted successfully",
        "payout_id": payout.id,
        "reference": payout.payout_reference,
        "amount": payout.amount,
        "state": payout.status
    }


@router.get("/payouts")
def list_my_seller_payouts(
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db)
):
    """Lists disbursement and settlement history for the current seller."""
    payouts = MarketplaceService.list_seller_payouts(db, seller.id)
    return [
        {
            "id": p.id,
            "amount": p.amount,
            "commission_deducted": p.commission_deducted,
            "net_amount": p.net_amount,
            "status": p.status,
            "reference": p.payout_reference,
            "period_start": p.period_start.isoformat() if p.period_start else None,
            "period_end": p.period_end.isoformat() if p.period_end else None,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in payouts
    ]


@router.get("/overview")
def get_marketplace_admin_overview(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Returns platform-wide vendor counts, marketplace GMV, and commission revenues (Admin only)."""
    return MarketplaceService.get_marketplace_overview(db)


@router.post("/payouts/{payout_id}/action")
def process_payout_disbursement_action(
    payout_id: int,
    data: PayoutActionSchema,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Approves, settles, or rejects a vendor payout disbursement (Admin only)."""
    payout = MarketplaceService.process_payout_disbursement(db, payout_id, data.action, data.reference)
    return {
        "payout_id": payout.id,
        "new_status": payout.status,
        "reference": payout.payout_reference,
        "message": f"Payout {payout_id} transitioned to {payout.status}"
    }


@router.get("/orders/{order_id}/split")
def get_order_seller_partition(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Returns multi-vendor partitioned sub-orders, commission deductions,
    and fulfillment packages for an order.
    """
    # Permission check: user must be customer or staff/admin
    user_roles = [ur.role.name for ur in current_user.roles if ur.role]
    split = OrderOrchestrationService.split_order_by_seller(db, order_id)
    if "ADMIN" not in user_roles and "SELLER" not in user_roles:
        if split["customer_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to inspect this order's vendor packages")
    return split


@router.get("/orders/{order_id}/items/{order_item_id}/return-eligibility")
def check_item_return_eligibility(
    order_id: int,
    order_item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Authenticates return policy compliance (30-day window, delivered status, non-duplicate return).
    """
    return OrderOrchestrationService.check_return_eligibility(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
        order_item_id=order_item_id
    )


@router.post("/orders/{order_id}/items/{order_item_id}/status")
def update_seller_order_item_status(
    order_id: int,
    order_item_id: int,
    data: ItemStatusUpdateSchema,
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db)
):
    """Updates status of a specific line item belonging to the authenticated vendor."""
    updated = OrderOrchestrationService.update_seller_item_status(
        db=db,
        seller_id=seller.id,
        order_item_id=order_item_id,
        new_status=data.status
    )
    return {
        "item_id": updated.id,
        "status": updated.status,
        "message": f"Item status updated to {updated.status}"
    }


@router.post("/ai-support/chat")
def ai_support_chat_inquiry(
    data: SupportChatRequest,
    db: Session = Depends(get_db)
):
    """
    Context-grounded AI Customer Support Assistant.
    Evaluates order tracking, return eligibility, product specs, and platform policies.
    """
    # Optional authentication resolution
    user_id = data.context.get("user_id") if data.context else None
    return AISupportService.process_customer_query(
        db=db,
        message=data.message,
        user_id=user_id,
        context=data.context
    )


@router.get("/pricing-recommendations")
def get_pricing_recommendations(
    seller: Seller = Depends(get_current_seller),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Retrieves AI dynamic pricing elasticity recommendations for the authenticated seller."""
    return DynamicPricingEngine.evaluate_seller_catalog(db, seller.id, limit=limit)


@router.get("/pricing-recommendations/product/{product_id}")
def get_product_pricing_recommendation(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Calculates optimal price, expected demand shift, and elasticity for a single product."""
    return DynamicPricingEngine.evaluate_product_pricing(db, product_id)

