"""
Seller & Seller Profile Models for Multi-Vendor Marketplace.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.base import TimestampMixin


class SellerStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"


class Seller(Base, TimestampMixin):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    store_name = Column(String(150), unique=True, index=True, nullable=False)
    legal_name = Column(String(200), nullable=False)
    business_email = Column(String(255), unique=True, nullable=False)
    business_phone = Column(String(30), nullable=False)
    tax_identifier = Column(String(50), nullable=True)  # GSTIN / VAT / EIN
    status = Column(String(20), default=SellerStatus.APPROVED.value, nullable=False, index=True)
    rating = Column(Float, default=5.0, nullable=False)
    total_sales_count = Column(Integer, default=0, nullable=False)
    commission_rate = Column(Float, default=0.10, nullable=False)  # 10% marketplace fee

    user = relationship("User", back_populates="seller_profile")
    profile = relationship("SellerProfile", back_populates="seller", uselist=False, cascade="all, delete-orphan")
    products = relationship("Product", back_populates="seller")
    orders = relationship("OrderItem", back_populates="seller")


class SellerProfile(Base, TimestampMixin):
    __tablename__ = "seller_profiles"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="CASCADE"), unique=True, nullable=False)
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    support_email = Column(String(255), nullable=True)
    return_policy = Column(Text, nullable=True)
    shipping_policy = Column(Text, nullable=True)

    seller = relationship("Seller", back_populates="profile")

# Banner image URL, verification status badge, and custom description fields
