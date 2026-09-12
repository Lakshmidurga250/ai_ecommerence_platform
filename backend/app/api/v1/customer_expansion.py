"""
Customer Expansion & Catalog API Router.
Exposes endpoints for:
- Product Bundles (Frequently Bought Together)
- Product Community Q&A
- Review Helpfulness Voting
- Recently Viewed Products
- Price & Back-in-Stock Alerts
- Inventory Stock Ledger
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.dependencies.auth import get_current_active_user, RoleChecker
from app.dependencies.tenant import get_current_seller, verify_seller_product_ownership
from app.models.user import User
from app.models.seller import Seller
from app.models.product import Product
from app.schemas.product import ProductRead
from app.services.catalog_expansion_service import CatalogExpansionService

router = APIRouter(tags=["Customer Experience & Catalog Expansion"])


# --- Schemas ---
class BundleCreateRequest(BaseModel):
    bundle_product_id: int
    bundle_name: str
    discount_percent: float = Field(default=10.0, ge=1.0, le=90.0)


class QuestionCreateRequest(BaseModel):
    question_text: str = Field(..., min_length=5, max_length=1000)


class AnswerCreateRequest(BaseModel):
    answer_text: str = Field(..., min_length=3, max_length=2000)


class ReviewVoteRequest(BaseModel):
    is_helpful: bool = True


class RecentlyViewedRequest(BaseModel):
    product_id: int


class PriceAlertCreateRequest(BaseModel):
    product_id: int
    target_price: float = Field(..., gt=0)
    alert_type: str = "PRICE_DROP"  # PRICE_DROP, BACK_IN_STOCK


class LedgerMovementRequest(BaseModel):
    transaction_type: str = Field(..., description="INWARD, RESERVATION, DISPATCH, RETURN, ADJUSTMENT")
    quantity_change: int
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    warehouse_id: Optional[int] = None


# --- Endpoints ---

# 1. Product Bundles
@router.get("/products/{product_id}/bundles")
def get_product_bundles(product_id: int, db: Session = Depends(get_db)):
    """Returns bundle pairings and bundle discounts for a primary product."""
    return CatalogExpansionService.get_bundles_for_product(db, product_id)


@router.post("/products/{product_id}/bundles", dependencies=[Depends(RoleChecker(["SELLER", "ADMIN"]))])
def create_product_bundle(
    product_id: int,
    payload: BundleCreateRequest,
    db: Session = Depends(get_db)
):
    """Configures a discounted product bundle pairing."""
    bundle = CatalogExpansionService.create_bundle(
        db=db,
        primary_product_id=product_id,
        bundle_product_id=payload.bundle_product_id,
        bundle_name=payload.bundle_name,
        discount_percent=payload.discount_percent
    )
    return {"message": "Bundle created successfully", "bundle_id": bundle.id}


# 2. Product Community Q&A
@router.get("/products/{product_id}/questions")
def get_product_questions(product_id: int, db: Session = Depends(get_db)):
    """Returns approved customer questions and verified answers for a product."""
    return CatalogExpansionService.get_questions_for_product(db, product_id)


@router.post("/products/{product_id}/questions")
def ask_product_question(
    product_id: int,
    payload: QuestionCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submits a customer question about a product."""
    q = CatalogExpansionService.ask_question(
        db=db,
        product_id=product_id,
        user_id=current_user.id,
        question_text=payload.question_text
    )
    return {"message": "Question submitted successfully", "question_id": q.id}


@router.post("/questions/{question_id}/answers")
def answer_product_question(
    question_id: int,
    payload: AnswerCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submits an answer to a product question."""
    user_roles = [ur.role.name for ur in current_user.roles if ur.role]
    is_seller = "SELLER" in user_roles or "ADMIN" in user_roles

    ans = CatalogExpansionService.answer_question(
        db=db,
        question_id=question_id,
        user_id=current_user.id,
        answer_text=payload.answer_text,
        is_seller_reply=is_seller
    )
    return {"message": "Answer posted successfully", "answer_id": ans.id}


# 3. Review Helpfulness Voting
@router.post("/reviews/{review_id}/vote")
def vote_review_helpfulness(
    review_id: int,
    payload: ReviewVoteRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Votes on the helpfulness of a customer review."""
    try:
        return CatalogExpansionService.vote_review(
            db=db,
            review_id=review_id,
            user_id=current_user.id,
            is_helpful=payload.is_helpful
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# 4. Recently Viewed Products
@router.get("/users/recently-viewed", response_model=List[ProductRead])
def get_recently_viewed_products(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Returns the authenticated customer's recently viewed products."""
    return CatalogExpansionService.get_recently_viewed(db, current_user.id)


@router.post("/users/recently-viewed")
def record_recently_viewed_product(
    payload: RecentlyViewedRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Records a product view in the customer's history."""
    CatalogExpansionService.record_recently_viewed(db, current_user.id, payload.product_id)
    return {"status": "recorded"}


# 5. Price & Stock Alerts
@router.get("/users/price-alerts")
def get_user_price_alerts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retrieves all active price and back-in-stock alerts for the user."""
    return CatalogExpansionService.get_user_alerts(db, current_user.id)


@router.post("/users/price-alerts")
def create_price_alert(
    payload: PriceAlertCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subscribes user to a price drop or back-in-stock alert."""
    alert = CatalogExpansionService.create_price_alert(
        db=db,
        user_id=current_user.id,
        product_id=payload.product_id,
        target_price=payload.target_price,
        alert_type=payload.alert_type
    )
    return {"message": "Alert set successfully", "alert_id": alert.id}


# 6. Inventory Stock Ledger
@router.get("/products/{product_id}/ledger", dependencies=[Depends(RoleChecker(["SELLER", "ADMIN"]))])
def get_product_stock_ledger(
    product_id: int,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller)
):
    """Retrieves the audit trail of stock movements for a specific product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Tenant isolation: Cannot view other seller's stock ledger")

    ledger = CatalogExpansionService.get_product_ledger(db, product_id)
    return [
        {
            "id": l.id,
            "transaction_type": l.transaction_type,
            "quantity_change": l.quantity_change,
            "balance_after": l.balance_after,
            "reference_id": l.reference_id,
            "notes": l.notes,
            "created_at": l.created_at.isoformat()
        }
        for l in ledger
    ]


@router.post("/products/{product_id}/ledger", dependencies=[Depends(RoleChecker(["SELLER", "ADMIN"]))])
def record_ledger_movement(
    product_id: int,
    payload: LedgerMovementRequest,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller)
):
    """Records an atomic stock movement entry in the inventory ledger."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Tenant isolation: Cannot modify other seller's inventory")

    entry = CatalogExpansionService.record_stock_ledger_movement(
        db=db,
        product_id=product_id,
        transaction_type=payload.transaction_type,
        quantity_change=payload.quantity_change,
        reference_id=payload.reference_id,
        notes=payload.notes,
        warehouse_id=payload.warehouse_id
    )
    return {
        "message": "Stock ledger updated successfully",
        "new_stock": entry.balance_after,
        "entry_id": entry.id
    }
