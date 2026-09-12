"""
Coupons & Promotional Discounts API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.cart import CouponCreate, CouponRead, CouponValidate
from app.services.coupon_service import CouponService

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.get("/", response_model=List[CouponRead])
def list_coupons(db: Session = Depends(get_db)):
    """List active promotional coupons."""
    return CouponService.list_coupons(db)


@router.post("/validate", response_model=CouponRead)
def validate_coupon(
    data: CouponValidate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate a coupon code against minimum order rules and user limits."""
    return CouponService.validate_coupon(db, data.code, current_user.id, data.cart_total)


@router.post("/", response_model=CouponRead, status_code=status.HTTP_201_CREATED)
def create_coupon(
    data: CouponCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Create a new promotional discount coupon (Admins only)."""
    return CouponService.create_coupon(db, data)
