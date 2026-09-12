"""
Analytical Star Schema Models for Data Warehouse & Business Intelligence.
Defines dimension tables (DimCustomer, DimProduct, DimSeller, DimDate)
and fact tables (FactSales, FactProductViews, FactOrderReturns).
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base


class DimDate(Base):
    __tablename__ = "dim_date"

    date_key = Column(Integer, primary_key=True, index=True)  # YYYYMMDD e.g. 20260912
    full_date = Column(Date, nullable=False, unique=True)
    day_of_week = Column(Integer, nullable=False)             # 1-7
    day_name = Column(String(16), nullable=False)             # Monday, etc.
    is_weekend = Column(Boolean, default=False)
    month = Column(Integer, nullable=False)                   # 1-12
    month_name = Column(String(16), nullable=False)           # September
    quarter = Column(Integer, nullable=False)                 # 1-4
    year = Column(Integer, nullable=False)                    # 2026


class DimCustomer(Base):
    __tablename__ = "dim_customer"

    customer_key = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, index=True, nullable=False)
    email = Column(String(255))
    full_name = Column(String(255))
    rfm_segment = Column(String(64), default="NEW_CUSTOMER")
    loyalty_tier = Column(String(32), default="BRONZE")
    historical_clv = Column(Float, default=0.0)
    city = Column(String(128))
    state = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)


class DimProduct(Base):
    __tablename__ = "dim_product"

    product_key = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, index=True, nullable=False)
    sku = Column(String(64))
    product_name = Column(String(255), nullable=False)
    category_name = Column(String(128))
    category_slug = Column(String(128))
    brand_name = Column(String(128))
    unit_cost = Column(Float, default=0.0)
    current_retail_price = Column(Float, nullable=False)
    price_tier = Column(String(32), default="MID_RANGE")
    quality_score = Column(Float, default=75.0)


class DimSeller(Base):
    __tablename__ = "dim_seller"

    seller_key = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, index=True, nullable=False)
    business_name = Column(String(255), nullable=False)
    commission_rate = Column(Float, default=0.10)
    rating = Column(Float, default=4.5)
    fulfillment_hub = Column(String(32), default="DEL")


class FactSales(Base):
    __tablename__ = "fact_sales"

    sales_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, index=True, nullable=False)
    order_item_id = Column(Integer, index=True)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), index=True)
    customer_key = Column(Integer, ForeignKey("dim_customer.customer_key"), index=True)
    product_key = Column(Integer, ForeignKey("dim_product.product_key"), index=True)
    seller_key = Column(Integer, ForeignKey("dim_seller.seller_key"), index=True)
    
    quantity_sold = Column(Integer, default=1)
    gross_revenue = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    net_revenue = Column(Float, nullable=False)
    estimated_cost = Column(Float, default=0.0)
    gross_profit = Column(Float, nullable=False)
    tax_collected = Column(Float, default=0.0)
    payment_method = Column(String(32), default="CARD")


class FactProductViews(Base):
    __tablename__ = "fact_product_views"

    view_id = Column(Integer, primary_key=True, autoincrement=True)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), index=True)
    product_key = Column(Integer, ForeignKey("dim_product.product_key"), index=True)
    customer_key = Column(Integer, ForeignKey("dim_customer.customer_key"), nullable=True)
    dwell_time_seconds = Column(Integer, default=15)
    added_to_cart = Column(Boolean, default=False)
    device_type = Column(String(32), default="DESKTOP")


class FactOrderReturns(Base):
    __tablename__ = "fact_order_returns"

    return_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, index=True, nullable=False)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), index=True)
    product_key = Column(Integer, ForeignKey("dim_product.product_key"), index=True)
    customer_key = Column(Integer, ForeignKey("dim_customer.customer_key"), index=True)
    return_reason = Column(String(128))
    refund_amount = Column(Float, nullable=False)
    restocking_fee = Column(Float, default=0.0)
    reverse_shipping_cost = Column(Float, default=120.0)
