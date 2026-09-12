"""
Tenant Isolation & Authorization Dependencies.
Guarantees object-level multi-tenant boundaries between sellers and customers.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.seller import Seller
from app.models.product import Product
from app.models.order import OrderItem


def get_current_seller(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Seller:
    """
    Resolves the seller entity for the authenticated user.
    Admin users can operate across sellers; standard sellers are bound to their seller account.
    """
    user_roles = [ur.role.name for ur in current_user.roles if ur.role]
    if "ADMIN" in user_roles:
        # Admins have full oversight; fetch primary or first seller context
        seller = db.query(Seller).filter(Seller.user_id == current_user.id).first()
        if not seller:
            # Fallback to system marketplace seller
            seller = db.query(Seller).first()
        return seller

    if "SELLER" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted: user does not hold verified seller privileges."
        )

    seller = db.query(Seller).filter(Seller.user_id == current_user.id).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller profile not initialized. Please complete vendor onboarding."
        )

    if seller.status not in ("APPROVED", "ACTIVE"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Seller store is {seller.status}. Operations are currently suspended."
        )

    return seller


def verify_seller_product_ownership(
    product_id: int,
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db)
) -> Product:
    """Verifies that the requested product belongs strictly to the authenticated seller."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )

    # If user is admin (seller.user_id matches admin or seller is fallback), permit
    if product.seller_id != seller.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant Isolation Error: You are not authorized to modify this catalog product."
        )

    return product
