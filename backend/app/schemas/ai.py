"""
AI, Recommendation, Search Parsing, Forecasting, Fraud, and Segmentation Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.schemas.product import ProductRead


class RecommendationItem(BaseModel):
    product: ProductRead
    score: float
    explanation: str  # e.g., "Because you viewed similar running shoes"
    model_type: str   # POPULARITY, CONTENT, COLLABORATIVE, HYBRID, NEURAL


class RecommendationResponse(BaseModel):
    user_id: Optional[int] = None
    strategy: str
    recommendations: List[RecommendationItem] = []


class ParsedSearchIntent(BaseModel):
    raw_query: str
    cleaned_query: str
    extracted_category: Optional[str] = None
    extracted_brand: Optional[str] = None
    extracted_color: Optional[str] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    extracted_attributes: Dict[str, Any] = {}
    is_semantic_intent: bool = False


class DemandForecastItem(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    predicted_demand_next_7_days: float
    predicted_demand_next_30_days: float
    reorder_recommended: bool
    recommended_reorder_units: int
    model_algorithm: str
    confidence_score: float
    evaluation_metrics: Dict[str, float]  # Real MAE, RMSE, MAPE


class FraudRiskEvaluation(BaseModel):
    order_id: int
    risk_score: float  # 0.0 to 100.0
    risk_level: str    # LOW, MEDIUM, HIGH, CRITICAL
    is_suspicious: bool
    trigger_reasons: List[str]
    suggested_action: str


class CustomerSegmentProfile(BaseModel):
    user_id: int
    segment_name: str  # BUDGET_BUYER, HIGH_VALUE_LOYAL, FREQUENT_BUYER, OCCASIONAL, AT_RISK
    recency_days: int
    order_frequency: int
    total_monetary_spend: float
    silhouette_score: float
    description: str


class ChurnRiskProfile(BaseModel):
    user_id: int
    churn_probability: float  # 0.0 to 1.0
    risk_category: str        # LOW, MEDIUM, HIGH
    contributing_factors: List[str]
    suggested_retention_action: str


class ShoppingAssistantRequest(BaseModel):
    user_message: str
    user_id: Optional[int] = None
    conversation_history: List[Dict[str, str]] = []


class ShoppingAssistantResponse(BaseModel):
    assistant_reply: str
    parsed_intent: ParsedSearchIntent
    grounded_products: List[ProductRead] = []
    confidence_score: float
    reasoning: str
