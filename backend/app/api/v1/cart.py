"""
Shopping Cart API Endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cart import CartRead, CartItemAdd, CartItemUpdate
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


@router.get("/", response_model=CartRead)
def get_cart(
    coupon_code: Optional[str] = Query(None, description="Optional coupon code to apply"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve current customer's shopping cart with price and tax breakdown."""
    cart_data = CartService.calculate_cart(db, current_user.id, coupon_code=coupon_code)
    return cart_data


@router.post("/items", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    data: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a product item or variant to shopping cart."""
    CartService.add_to_cart(db, current_user.id, data.product_id, data.quantity, data.variant_id)
    return CartService.calculate_cart(db, current_user.id)


@router.put("/items/{item_id}", response_model=CartRead)
def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update item quantity in cart."""
    CartService.update_cart_item(db, current_user.id, item_id, data.quantity)
    return CartService.calculate_cart(db, current_user.id)


@router.delete("/items/{item_id}", response_model=CartRead)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove an item from cart."""
    CartService.remove_cart_item(db, current_user.id, item_id)
    return CartService.calculate_cart(db, current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Empty the current shopping cart."""
    CartService.clear_cart(db, current_user.id)
