"""
Coupon & Promotional Discount Service.
Handles coupon creation, activation, validation, and usage limits.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException, AppException
from app.models.cart import Coupon, CouponUsage
from app.schemas.cart import CouponCreate


class CouponService:
    @staticmethod
    def create_coupon(db: Session, data: CouponCreate) -> Coupon:
        code_clean = data.code.strip().upper()
        existing = db.query(Coupon).filter(Coupon.code == code_clean).first()
        if existing:
            raise ConflictException(f"Coupon code '{code_clean}' already exists")

        coupon = Coupon(
            code=code_clean,
            discount_type=data.discount_type,
            discount_value=data.discount_value,
            min_order_amount=data.min_order_amount,
            max_discount_amount=data.max_discount_amount,
            usage_limit=data.usage_limit,
            per_user_limit=data.per_user_limit,
            valid_until=data.valid_until,
            is_active=True
        )
        db.add(coupon)
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def validate_coupon(db: Session, code: str, user_id: int, order_amount: float) -> Coupon:
        code_clean = code.strip().upper()
        coupon = db.query(Coupon).filter(Coupon.code == code_clean).first()
        if not coupon or not coupon.is_active:
            raise AppException("Invalid or inactive coupon code", 400, "INVALID_COUPON")

        now = datetime.now(timezone.utc)
        if coupon.valid_until and coupon.valid_until.replace(tzinfo=timezone.utc) < now:
            raise AppException("This coupon has expired", 400, "COUPON_EXPIRED")

        if order_amount < coupon.min_order_amount:
            raise AppException(f"Minimum order value of ₹{coupon.min_order_amount} required for this coupon", 400, "MIN_ORDER_NOT_MET")

        if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
            raise AppException("Coupon usage limit has been reached", 400, "COUPON_LIMIT_REACHED")

        user_usage = db.query(CouponUsage).filter(CouponUsage.coupon_id == coupon.id, CouponUsage.user_id == user_id).count()
        if user_usage >= coupon.per_user_limit:
            raise AppException(f"You have already used this coupon the maximum allowed {coupon.per_user_limit} time(s)", 400, "PER_USER_LIMIT_REACHED")

        return coupon

    @staticmethod
    def list_coupons(db: Session) -> List[Coupon]:
        return db.query(Coupon).all()

# Comprehensive coupon rule validator engine
