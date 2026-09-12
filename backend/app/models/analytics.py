"""
Behavioral Tracking, AI Inferences, Forecasts, Fraud Alerts, and Model Registry Models.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class BehaviorEvent(Base, TimestampMixin):
    __tablename__ = "behavior_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # VIEW, SEARCH, CLICK, CART_ADD, CART_REMOVE, WISHLIST, PURCHASE
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    event_metadata = Column(JSON, default=dict, nullable=False)

    product = relationship("Product")
    category = relationship("Category")


class SearchEvent(Base, TimestampMixin):
    __tablename__ = "search_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    query_text = Column(String(255), nullable=False, index=True)
    parsed_intent = Column(JSON, default=dict, nullable=False)
    results_count = Column(Integer, default=0, nullable=False)
    selected_product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)


class RecommendationLog(Base, TimestampMixin):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    model_type = Column(String(50), nullable=False)  # POPULARITY, CONTENT, COLLABORATIVE, HYBRID, NEURAL
    recommended_product_ids = Column(JSON, nullable=False)
    clicked_product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)


class DemandForecast(Base, TimestampMixin):
    __tablename__ = "demand_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    forecast_date = Column(DateTime, nullable=False, index=True)
    horizon_days = Column(Integer, default=7, nullable=False)
    predicted_demand = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=True)
    upper_bound = Column(Float, nullable=True)
    confidence_score = Column(Float, default=0.90, nullable=False)
    model_version = Column(String(50), nullable=False)
    actual_demand = Column(Float, nullable=True)

    product = relationship("Product")


class FraudAlert(Base, TimestampMixin):
    __tablename__ = "fraud_alerts"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    risk_score = Column(Float, nullable=False, index=True)  # 0.0 to 100.0
    risk_level = Column(String(20), default="LOW", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    trigger_reasons = Column(JSON, default=list, nullable=False)
    status = Column(String(30), default="PENDING_REVIEW", nullable=False, index=True)  # PENDING_REVIEW, APPROVED, BLOCKED
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    order = relationship("Order")
    user = relationship("User", foreign_keys=[user_id])


class CustomerSegment(Base, TimestampMixin):
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    segment_name = Column(String(50), nullable=False, index=True)  # BUDGET_BUYER, HIGH_VALUE_LOYAL, FREQUENT_BUYER, AT_RISK
    rfm_metrics = Column(JSON, default=dict, nullable=False)  # {"recency_days": 12, "frequency": 5, "monetary": 14200.0}
    cluster_id = Column(Integer, default=0, nullable=False)

    user = relationship("User")


class ChurnPrediction(Base, TimestampMixin):
    __tablename__ = "churn_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    churn_probability = Column(Float, nullable=False, index=True)  # 0.0 to 1.0
    risk_category = Column(String(20), default="LOW", nullable=False)  # LOW, MEDIUM, HIGH
    contributing_factors = Column(JSON, default=list, nullable=False)
    recommended_action = Column(String(255), nullable=True)

    user = relationship("User")


class ModelRegistryEntry(Base, TimestampMixin):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), index=True, nullable=False)
    version = Column(String(50), index=True, nullable=False)
    algorithm = Column(String(100), nullable=False)
    dataset_version = Column(String(50), nullable=False)
    hyperparameters = Column(JSON, default=dict, nullable=False)
    metrics = Column(JSON, default=dict, nullable=False)  # e.g., {"mae": 1.2, "rmse": 2.1, "accuracy": 0.94}
    artifact_path = Column(String(500), nullable=True)
    status = Column(String(30), default="PRODUCTION", nullable=False, index=True)  # TRAINED, STAGING, PRODUCTION, RETIRED
