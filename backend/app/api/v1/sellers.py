"""
Seller Management API Endpoints for Multi-Vendor Marketplace.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.seller import SellerRegister, SellerRead, SellerProfileUpdate, SellerProfileRead
from app.schemas.analytics import SellerDashboardMetrics
from app.services.seller_service import SellerService
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/sellers", tags=["Seller Management"])


@router.post("/register", response_model=SellerRead, status_code=status.HTTP_201_CREATED)
def register_seller(
    data: SellerRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Onboard current user as a marketplace seller."""
    return SellerService.register_seller(db, current_user, data)


@router.get("/me", response_model=SellerRead)
def get_my_seller_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Get the authenticated seller's store profile and metrics."""
    return SellerService.get_seller_by_user_id(db, current_user.id)


@router.put("/profile", response_model=SellerProfileRead)
def update_store_profile(
    data: SellerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER"]))
):
    """Update seller storefront branding, return policy, and description."""
    seller = SellerService.get_seller_by_user_id(db, current_user.id)
    return SellerService.update_seller_profile(db, seller.id, data)


@router.get("/analytics", response_model=SellerDashboardMetrics)
def get_seller_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER"]))
):
    """Get seller isolated revenue, order counts, and low-stock alerts."""
    seller = SellerService.get_seller_by_user_id(db, current_user.id)
    return AnalyticsService.get_seller_metrics(db, seller.id)


@router.get("/{seller_id}", response_model=SellerRead)
def get_public_seller_profile(seller_id: int, db: Session = Depends(get_db)):
    """Publicly viewable seller storefront details."""
    return SellerService.get_seller_by_id(db, seller_id)


@router.get("/", response_model=List[SellerRead])
def list_sellers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List approved marketplace sellers."""
    return SellerService.list_sellers(db, skip, limit)
