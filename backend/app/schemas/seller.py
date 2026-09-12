"""
Seller & Seller Profile Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SellerRegister(BaseModel):
    store_name: str
    legal_name: str
    business_email: EmailStr
    business_phone: str
    tax_identifier: Optional[str] = None
    description: Optional[str] = None


class SellerUpdate(BaseModel):
    legal_name: Optional[str] = None
    business_phone: Optional[str] = None
    tax_identifier: Optional[str] = None


class SellerProfileUpdate(BaseModel):
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    support_email: Optional[EmailStr] = None
    return_policy: Optional[str] = None
    shipping_policy: Optional[str] = None


class SellerProfileRead(BaseModel):
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    support_email: Optional[str] = None
    return_policy: Optional[str] = None
    shipping_policy: Optional[str] = None

    class Config:
        from_attributes = True


class SellerRead(BaseModel):
    id: int
    user_id: int
    store_name: str
    legal_name: str
    business_email: str
    business_phone: str
    tax_identifier: Optional[str] = None
    status: str
    rating: float
    total_sales_count: int
    commission_rate: float
    profile: Optional[SellerProfileRead] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SellerStatusUpdate(BaseModel):
    status: str  # APPROVED, SUSPENDED, REJECTED
