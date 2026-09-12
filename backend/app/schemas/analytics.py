"""
Business Analytics, Dashboard Metrics, and Audit Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class BusinessOverviewMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    total_sellers: int
    total_products: int
    average_order_value: float
    pending_orders_count: int
    low_stock_items_count: int
    fraud_alerts_count: int
    revenue_chart_data: List[Dict[str, Any]] = []
    top_selling_products: List[Dict[str, Any]] = []
    category_distribution: List[Dict[str, Any]] = []


class SellerDashboardMetrics(BaseModel):
    seller_id: int
    store_name: str
    total_revenue: float
    total_orders: int
    total_products: int
    average_order_value: float
    low_stock_count: int
    sales_trend: List[Dict[str, Any]] = []
    top_products: List[Dict[str, Any]] = []


class AuditLogRead(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    status: str
    details: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class BehaviorEventCreate(BaseModel):
    event_type: str  # VIEW, SEARCH, CLICK, CART_ADD, CART_REMOVE, WISHLIST, PURCHASE
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = {}
