"""
Cart, Wishlist, and Coupon Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.product import ProductRead


class CartItemAdd(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemRead(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    price_at_addition: float
    product: Optional[ProductRead] = None

    class Config:
        from_attributes = True


class CartRead(BaseModel):
    id: int
    user_id: int
    items: List[CartItemRead] = []
    subtotal: float
    tax_amount: float
    discount_amount: float
    shipping_fee: float
    total_amount: float
    coupon_code: Optional[str] = None


class WishlistItemAdd(BaseModel):
    product_id: int


class WishlistItemRead(BaseModel):
    id: int
    product_id: int
    product: Optional[ProductRead] = None

    class Config:
        from_attributes = True


class WishlistRead(BaseModel):
    id: int
    user_id: int
    items: List[WishlistItemRead] = []

    class Config:
        from_attributes = True


class CouponValidate(BaseModel):
    code: str
    cart_total: float


class CouponCreate(BaseModel):
    code: str
    discount_type: str = "PERCENTAGE"  # PERCENTAGE, FIXED
    discount_value: float = Field(..., gt=0)
    min_order_amount: float = 0.0
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    per_user_limit: int = 1
    valid_until: Optional[datetime] = None


class CouponRead(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: float
    min_order_amount: float
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_count: int
    is_active: bool
    valid_from: datetime
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True
