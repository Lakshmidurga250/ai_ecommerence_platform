"""
Order Management & Checkout API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.order import OrderRead, CheckoutRequest, OrderStatusUpdate
from app.services.order_service import OrderService
from app.services.seller_service import SellerService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def checkout(
    data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute complete checkout pipeline: stock reservation, order placement, payment simulation, and shipment."""
    return OrderService.checkout(db, current_user.id, data)


@router.get("/", response_model=List[OrderRead])
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List purchase history for current customer."""
    return OrderService.list_customer_orders(db, current_user.id)


@router.get("/seller", response_model=List[OrderRead])
def list_seller_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """List orders containing items belonging to current seller."""
    seller = SellerService.get_seller_by_user_id(db, current_user.id)
    return OrderService.list_seller_orders(db, seller.id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get full details of a specific order."""
    is_admin = "ADMIN" in current_user.role_names
    seller = db.query(User).filter(User.id == current_user.id).first().seller_profile
    seller_id = seller.id if seller else None
    return OrderService.get_order_by_id(db, order_id, user_id=current_user.id, seller_id=seller_id, is_admin=is_admin)


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Transition order status through fulfillment lifecycle."""
    is_admin = "ADMIN" in current_user.role_names
    seller = current_user.seller_profile
    seller_id = seller.id if seller else None
    return OrderService.update_order_status(db, order_id, data.status, seller_id=seller_id, is_admin=is_admin)
