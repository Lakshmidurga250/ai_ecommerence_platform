"""
V3 Advanced Recommendation Routers.
Exposes AI Outfit Generator, Tiered Bundles, Personalized Ranking, Session Recommendations, and Cross-Sell/Upsell.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product, Category
from app.schemas.expansion_v3 import (
    PersonalizedRankingRequest, SessionRecommendationRequest
)
from ai.recommendations.outfit_bundle_generator import OutfitBundleGenerator
from ai.recommendations.bundle_recommender import BundleRecommender
from ai.recommendations.personalized_ranker import PersonalizedRanker
from ai.recommendations.session_recommender import SessionRecommender
from ai.recommendations.cross_sell_upsell import CrossSellUpsellPredictor

router = APIRouter(prefix="/recommendations-v3", tags=["Recommendations V3"])


@router.get("/outfit/{product_id}")
def generate_product_outfit(
    product_id: int,
    bundle_size: int = Query(3, ge=2, le=5),
    discount_pct: float = Query(12.0, ge=0.0, le=40.0),
    db: Session = Depends(get_db)
):
    """
    Generates compatible multi-product outfits / setups centered on a focal item.
    """
    generator = OutfitBundleGenerator(db)
    result = generator.generate_outfit_for_product(
        product_id=product_id,
        bundle_size=bundle_size,
        discount_percentage=discount_pct,
        db=db
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/bundles/{product_id}")
def generate_tiered_bundles(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Generates 3-tier bundles (Starter, Pro Ecosystem, Master Bundle) with dynamic bundle savings.
    """
    recommender = BundleRecommender(db)
    result = recommender.generate_tiered_bundles(product_id=product_id, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/personalized-ranking")
def personalized_product_ranking(
    payload: PersonalizedRankingRequest,
    db: Session = Depends(get_db)
):
    """
    Re-ranks candidate products tailored specifically for a customer's affinities.
    """
    query = db.query(Product).filter(Product.is_active == True)
    if payload.product_ids:
        query = query.filter(Product.id.in_(payload.product_ids))
    elif payload.category_slug:
        query = query.join(Category).filter(Category.slug == payload.category_slug)
    else:
        query = query.limit(40)

    candidates = query.all()
    ranker = PersonalizedRanker(db)
    ranked = ranker.rank_products_for_user(
        products=candidates,
        user_id=payload.user_id,
        limit=payload.limit or 20,
        db=db
    )
    return {
        "user_id": payload.user_id,
        "total_evaluated": len(candidates),
        "ranked_results": ranked
    }


@router.post("/session-recommendations")
def recommend_for_browsing_session(
    payload: SessionRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Predicts next items of interest conditioned on the customer's current browsing session.
    """
    recommender = SessionRecommender(db)
    return recommender.recommend_for_session(
        session_product_ids=payload.session_product_ids,
        limit=payload.limit or 6,
        db=db
    )


@router.get("/cross-sell/{product_id}")
def get_cross_sell_recommendations(
    product_id: int,
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Returns frequently bought together items with co-occurrence lift scores.
    """
    predictor = CrossSellUpsellPredictor(db)
    result = predictor.predict_cross_sell(product_id=product_id, limit=limit, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/upsell/{product_id}")
def get_upsell_recommendations(
    product_id: int,
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Identifies superior premium trade-up alternatives within the same category.
    """
    predictor = CrossSellUpsellPredictor(db)
    result = predictor.predict_upsell(product_id=product_id, limit=limit, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
