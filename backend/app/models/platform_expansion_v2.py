"""
SQLAlchemy Relational Models for AI Commerce Intelligence Platform V2.
Includes:
- A/B Testing & Experimentation (ABExperiment, ABExperimentEvent)
- Loyalty & Customer Rewards (LoyaltyAccount, LoyaltyTransaction)
- Dynamic Pricing Intelligence (DynamicPriceRecommendation)
- Smart Logistics & Routing (ShipmentRouteOptimization)
- MLOps Model Drift Monitoring (ModelDriftLog)
- Catalog Quality Auditing (ProductQualityAudit)
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text, Float, DateTime, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class ABExperiment(Base, TimestampMixin):
    __tablename__ = "ab_experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    traffic_split_ratio = Column(Float, default=0.5, nullable=False)  # 0.5 = 50% Control, 50% Variant
    status = Column(String(30), default="RUNNING", nullable=False, index=True)  # DRAFT, RUNNING, CONCLUDED, PAUSED
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time = Column(DateTime, nullable=True)
    target_metric = Column(String(50), default="conversion_rate", nullable=False)  # conversion_rate, ctr, aov, revenue
    control_config = Column(JSON, default=dict, nullable=False)
    variant_config = Column(JSON, default=dict, nullable=False)

    events = relationship("ABExperimentEvent", back_populates="experiment", cascade="all, delete-orphan")


class ABExperimentEvent(Base, TimestampMixin):
    __tablename__ = "ab_experiment_events"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("ab_experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    variant = Column(String(20), nullable=False, index=True)  # CONTROL, VARIANT
    event_type = Column(String(50), nullable=False, index=True)  # IMPRESSION, CLICK, CONVERSION, REVENUE
    value = Column(Float, default=1.0, nullable=False)  # e.g., purchase value or 1.0 for count
    event_metadata = Column(JSON, default=dict, nullable=False)

    experiment = relationship("ABExperiment", back_populates="events")


class LoyaltyAccount(Base, TimestampMixin):
    __tablename__ = "loyalty_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    points_balance = Column(Integer, default=0, nullable=False)
    tier = Column(String(30), default="BRONZE", nullable=False, index=True)  # BRONZE, SILVER, GOLD, PLATINUM, DIAMOND
    lifetime_points = Column(Integer, default=0, nullable=False)
    lifetime_spend = Column(Float, default=0.0, nullable=False)

    user = relationship("User")
    transactions = relationship("LoyaltyTransaction", back_populates="account", cascade="all, delete-orphan")


class LoyaltyTransaction(Base, TimestampMixin):
    __tablename__ = "loyalty_transactions"

    id = Column(Integer, primary_key=True, index=True)
    loyalty_account_id = Column(Integer, ForeignKey("loyalty_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    points_delta = Column(Integer, nullable=False)  # Positive for earn, negative for redeem
    transaction_type = Column(String(50), nullable=False)  # PURCHASE_EARN, REWARD_REDEMPTION, WELCOME_BONUS, REVIEW_BONUS
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    notes = Column(String(255), nullable=True)

    account = relationship("LoyaltyAccount", back_populates="transactions")


class DynamicPriceRecommendation(Base, TimestampMixin):
    __tablename__ = "dynamic_price_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False, index=True)
    current_price = Column(Float, nullable=False)
    recommended_price = Column(Float, nullable=False)
    expected_demand_lift = Column(Float, nullable=False)  # e.g., +14.5%
    confidence_score = Column(Float, default=0.85, nullable=False)
    elasticity_score = Column(Float, default=-1.2, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False, index=True)  # PENDING, APPLIED, DISMISSED
    rationale = Column(Text, nullable=True)

    product = relationship("Product")
    seller = relationship("Seller")


class ShipmentRouteOptimization(Base, TimestampMixin):
    __tablename__ = "shipment_route_optimizations"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    carrier_name = Column(String(100), nullable=False)  # BlueDart Express, Delhivery Logistics, DTDC Air
    estimated_transit_days = Column(Integer, default=2, nullable=False)
    shipping_cost = Column(Float, default=0.0, nullable=False)
    risk_level = Column(String(20), default="LOW", nullable=False)  # LOW, MEDIUM, HIGH
    routing_metadata = Column(JSON, default=dict, nullable=False)

    order = relationship("Order")
    warehouse = relationship("Warehouse")


class ModelDriftLog(Base, TimestampMixin):
    __tablename__ = "model_drift_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    feature_drift_score = Column(Float, default=0.0, nullable=False)  # e.g., PSI or divergence
    prediction_drift_score = Column(Float, default=0.0, nullable=False)
    status = Column(String(30), default="NORMAL", nullable=False, index=True)  # NORMAL, WARNING, CRITICAL
    drift_details = Column(JSON, default=dict, nullable=False)
    recommended_action = Column(String(255), nullable=True)


class ProductQualityAudit(Base, TimestampMixin):
    __tablename__ = "product_quality_audits"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    quality_score = Column(Float, nullable=False)  # 0 to 100
    completeness_score = Column(Float, nullable=False)
    missing_attributes = Column(JSON, default=list, nullable=False)
    recommendations = Column(JSON, default=list, nullable=False)
    audited_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    product = relationship("Product")
