"""
Order, OrderItem, Payment, Shipment, ShipmentEvent, Return, and ReturnItem Models.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.base import TimestampMixin


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURN_REQUESTED = "RETURN_REQUESTED"
    RETURNED = "RETURNED"
    REFUNDED = "REFUNDED"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), nullable=False)
    
    status = Column(String(50), default=OrderStatus.PENDING.value, nullable=False, index=True)
    subtotal = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    shipping_fee = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    coupon_code = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)

    customer = relationship("User", back_populates="orders")
    shipping_address = relationship("Address")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    shipment = relationship("Shipment", back_populates="order", uselist=False, cascade="all, delete-orphan")
    returns = relationship("Return", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    product_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(50), default="CONFIRMED", nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    seller = relationship("Seller", back_populates="orders")


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    payment_method = Column(String(50), default="CARD", nullable=False)  # CARD, UPI, NET_BANKING, COD
    status = Column(String(50), default=PaymentStatus.PENDING.value, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    simulation_metadata = Column(JSON, default=dict, nullable=False)  # Mock gateway response

    order = relationship("Order", back_populates="payments")


class Shipment(Base, TimestampMixin):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    carrier_name = Column(String(100), default="Express Logistics", nullable=False)
    tracking_number = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(50), default="PREPARING", nullable=False)
    estimated_delivery = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="shipment")
    events = relationship("ShipmentEvent", back_populates="shipment", cascade="all, delete-orphan")


class ShipmentEvent(Base, TimestampMixin):
    __tablename__ = "shipment_events"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(100), nullable=False)
    location = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    event_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    shipment = relationship("Shipment", back_populates="events")


class Return(Base, TimestampMixin):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = Column(String(50), default="REQUESTED", nullable=False)  # REQUESTED, APPROVED, REJECTED, REFUNDED
    reason = Column(String(255), nullable=False)
    resolution_notes = Column(Text, nullable=True)
    refund_amount = Column(Float, default=0.0, nullable=False)

    order = relationship("Order", back_populates="returns")
    items = relationship("ReturnItem", back_populates="return_order", cascade="all, delete-orphan")


class ReturnItem(Base, TimestampMixin):
    __tablename__ = "return_items"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(Integer, ForeignKey("returns.id", ondelete="CASCADE"), nullable=False, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    reason = Column(String(255), nullable=True)

    return_order = relationship("Return", back_populates="items")
    order_item = relationship("OrderItem")
