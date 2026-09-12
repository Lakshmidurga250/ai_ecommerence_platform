"""
Customer Wishlist API Endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cart import WishlistRead, WishlistItemAdd, CartRead
from app.services.cart_service import CartService

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/", response_model=WishlistRead)
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve current customer's saved wishlist items."""
    return CartService.get_or_create_wishlist(db, current_user.id)


@router.post("/items", response_model=WishlistRead, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    data: WishlistItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save a product to customer's wishlist."""
    return CartService.add_to_wishlist(db, current_user.id, data.product_id)


@router.delete("/items/{product_id}", response_model=WishlistRead)
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a product from wishlist."""
    return CartService.remove_from_wishlist(db, current_user.id, product_id)


@router.post("/move-to-cart/{product_id}", response_model=CartRead)
def move_item_to_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Move an item from wishlist into the active shopping cart."""
    CartService.move_to_cart(db, current_user.id, product_id)
    return CartService.calculate_cart(db, current_user.id)
