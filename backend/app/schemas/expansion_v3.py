"""
Pydantic Schemas for V3 Platform Expansion:
15 Master AI Features & Deep Commerce Architecture.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# 1. Outfit & Bundles
class OutfitGenerationRequest(BaseModel):
    product_id: int
    bundle_size: Optional[int] = 3
    discount_percentage: Optional[float] = 12.0


class PersonalizedRankingRequest(BaseModel):
    product_ids: Optional[List[int]] = None
    category_slug: Optional[str] = None
    user_id: Optional[int] = None
    limit: Optional[int] = 20


class SessionRecommendationRequest(BaseModel):
    session_product_ids: List[int]
    limit: Optional[int] = 6


# 2. Promotion & Pricing
class PromotionOptimizationRequest(BaseModel):
    product_id: int
    unit_cost_estimate: Optional[float] = None
    baseline_weekly_sales: Optional[int] = 25
    target_objective: Optional[str] = "MAX_PROFIT"  # MAX_PROFIT or MAX_REVENUE


# 3. Quality & Review
class ReviewQualityCheckRequest(BaseModel):
    comment: str
    rating: int
    is_verified_purchase: Optional[bool] = True


# 4. Logistics & TSP
class RouteOptimizationRequest(BaseModel):
    origin_hub: str = "DEL"
    destination_hub: str = "BLR"


class TSPSequenceRequest(BaseModel):
    stop_codes: List[str]


# 5. Return Eligibility
class ReturnEligibilityRequest(BaseModel):
    order_id: int
    product_id: int
    return_reason: str


# 6. Semantic Search
class SemanticSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    min_score: Optional[float] = 0.10
