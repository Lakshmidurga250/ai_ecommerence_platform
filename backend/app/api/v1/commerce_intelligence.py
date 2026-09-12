"""
V3 Commerce Intelligence Routers.
Exposes Promotion Optimization, Next-Best-Action, Product Quality Scoring, Review Spam Detection, and Returns Governance.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.expansion_v3 import (
    PromotionOptimizationRequest, ReviewQualityCheckRequest, ReturnEligibilityRequest
)
from ai.pricing.promotion_optimizer import PromotionOptimizer
from ai.customer_intelligence.next_best_action import NextBestActionEngine
from ai.sentiment.product_quality_scorer import ProductQualityScorer
from ai.sentiment.review_quality_detector import ReviewQualityDetector
from app.services.returns_intelligence_service import ReturnsIntelligenceService

router = APIRouter(prefix="/commerce", tags=["Commerce Intelligence V3"])


@router.post("/promotion-optimize")
def optimize_product_promotion(
    payload: PromotionOptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Simulates demand shifts across discount tiers and returns optimal promotional discount.
    """
    optimizer = PromotionOptimizer(db)
    result = optimizer.optimize_promotion(
        product_id=payload.product_id,
        unit_cost_estimate=payload.unit_cost_estimate,
        baseline_weekly_sales=payload.baseline_weekly_sales or 25,
        target_objective=payload.target_objective or "MAX_PROFIT",
        db=db
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/next-best-action/{user_id}")
def get_customer_next_best_action(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Predicts the single highest-impact customer engagement / commercial action.
    """
    nba = NextBestActionEngine(db)
    result = nba.predict_next_best_action(user_id=user_id, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/product-quality/{product_id}")
def get_product_quality_score(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Computes holistic 0-100 quality index from Bayesian rating, sentiment, and return rate.
    """
    scorer = ProductQualityScorer(db)
    result = scorer.calculate_quality_score(product_id=product_id, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/review-quality-check")
def check_review_quality_and_spam(
    payload: ReviewQualityCheckRequest
):
    """
    Evaluates review text depth, lexical diversity, and spam probability.
    """
    detector = ReviewQualityDetector()
    return detector.evaluate_review_quality(
        comment=payload.comment,
        rating=payload.rating,
        is_verified_purchase=payload.is_verified_purchase if payload.is_verified_purchase is not None else True
    )


@router.get("/returns-dashboard")
def get_returns_intelligence_dashboard(
    db: Session = Depends(get_db)
):
    """
    Returns platform-wide returns KPIs, top return reasons, and category risk tiers.
    """
    service = ReturnsIntelligenceService(db)
    return service.get_returns_dashboard(db=db)


@router.post("/return-eligibility")
def evaluate_order_return_eligibility(
    payload: ReturnEligibilityRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluates 30-day return policy and generates risk score for an incoming return request.
    """
    service = ReturnsIntelligenceService(db)
    result = service.evaluate_return_eligibility(
        order_id=payload.order_id,
        product_id=payload.product_id,
        return_reason=payload.return_reason,
        db=db
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
