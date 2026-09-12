"""
SQLAlchemy Models Package.
Exports Base and all database models.
"""

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user import Role, User, UserRole, UserProfile, Address
from app.models.seller import Seller, SellerProfile, SellerStatus
from app.models.product import Category, Brand, Product, ProductVariant, ProductImage
from app.models.inventory import Warehouse, Inventory, InventoryMovement
from app.models.cart import Cart, CartItem, Wishlist, WishlistItem, Coupon, CouponUsage
from app.models.order import Order, OrderItem, Payment, Shipment, ShipmentEvent, Return, ReturnItem, OrderStatus, PaymentStatus
from app.models.review import Review, ReviewSentiment
from app.models.support import SupportTicket, SupportMessage
from app.models.analytics import (
    BehaviorEvent, SearchEvent, RecommendationLog, DemandForecast,
    FraudAlert, CustomerSegment, ChurnPrediction, ModelRegistryEntry
)
from app.models.audit import AuditLog

__all__ = [
    "Base",
    "TimestampMixin",
    "Role",
    "User",
    "UserRole",
    "UserProfile",
    "Address",
    "Seller",
    "SellerProfile",
    "SellerStatus",
    "Category",
    "Brand",
    "Product",
    "ProductVariant",
    "ProductImage",
    "Warehouse",
    "Inventory",
    "InventoryMovement",
    "Cart",
    "CartItem",
    "Wishlist",
    "WishlistItem",
    "Coupon",
    "CouponUsage",
    "Order",
    "OrderItem",
    "Payment",
    "Shipment",
    "ShipmentEvent",
    "Return",
    "ReturnItem",
    "OrderStatus",
    "PaymentStatus",
    "Review",
    "ReviewSentiment",
    "SupportTicket",
    "SupportMessage",
    "BehaviorEvent",
    "SearchEvent",
    "RecommendationLog",
    "DemandForecast",
    "FraudAlert",
    "CustomerSegment",
    "ChurnPrediction",
    "ModelRegistryEntry",
    "AuditLog"
]
