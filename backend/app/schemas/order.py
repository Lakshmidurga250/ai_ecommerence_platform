"""
Order, Payment, Shipping, and Return Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import AddressRead


class CheckoutRequest(BaseModel):
    shipping_address_id: int
    payment_method: str = "CARD"  # CARD, UPI, NET_BANKING, COD
    coupon_code: Optional[str] = None
    customer_notes: Optional[str] = None


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int] = None
    seller_id: int
    product_name: str
    sku: str
    unit_price: float
    quantity: int
    subtotal: float
    tax_amount: float
    total: float
    status: str

    model_config = ConfigDict(from_attributes=True)


class ShipmentEventRead(BaseModel):
    id: int
    status: str
    location: str
    description: Optional[str] = None
    event_time: datetime

    model_config = ConfigDict(from_attributes=True)


class ShipmentRead(BaseModel):
    id: int
    carrier_name: str
    tracking_number: str
    status: str
    estimated_delivery: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    events: List[ShipmentEventRead] = []

    model_config = ConfigDict(from_attributes=True)


class PaymentRead(BaseModel):
    id: int
    transaction_id: str
    payment_method: str
    status: str
    amount: float
    currency: str
    simulation_metadata: Dict[str, Any] = {}
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    order_number: str
    customer_id: int
    shipping_address_id: int
    status: str
    subtotal: float
    discount_amount: float
    tax_amount: float
    shipping_fee: float
    total_amount: float
    coupon_code: Optional[str] = None
    notes: Optional[str] = None
    shipping_address: Optional[AddressRead] = None
    items: List[OrderItemRead] = []
    payments: List[PaymentRead] = []
    shipment: Optional[ShipmentRead] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: str  # CONFIRMED, PROCESSING, PACKED, SHIPPED, OUT_FOR_DELIVERY, DELIVERED, CANCELLED


class PaymentSimulateRequest(BaseModel):
    order_id: int
    payment_method: str = "CARD"
    simulate_failure: bool = False


class PaymentSimulationResponse(BaseModel):
    transaction_id: str
    status: str
    amount: float
    currency: str
    simulated: bool = True
    message: str


class ReturnRequestCreate(BaseModel):
    order_id: int
    order_item_id: int
    quantity: int = Field(default=1, ge=1)
    reason: str


class ReturnRead(BaseModel):
    id: int
    order_id: int
    user_id: int
    status: str
    reason: str
    resolution_notes: Optional[str] = None
    refund_amount: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Round to 2 decimal places to avoid IEEE floating point inaccuracies
