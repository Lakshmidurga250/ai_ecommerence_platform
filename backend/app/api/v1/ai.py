"""
Artificial Intelligence & Machine Learning API Endpoints.
Provides recommendations, natural language search parsing, time-series forecasting,
fraud anomaly scoring, customer RFM segmentation, churn modeling, and grounded shopping assistant.
"""

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.dependencies.auth import get_optional_current_user, get_current_user, RoleChecker
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.review import Review
from app.models.analytics import DemandForecast, FraudAlert, CustomerSegment, ChurnPrediction, ModelRegistryEntry
from app.schemas.ai import (
    RecommendationResponse, RecommendationItem, ParsedSearchIntent,
    DemandForecastItem, FraudRiskEvaluation, CustomerSegmentProfile,
    ChurnRiskProfile, ShoppingAssistantRequest, ShoppingAssistantResponse
)
from app.schemas.product import ProductRead
from ai.recommendations.recommender import recommender_engine
from ai.recommendations.ranking_pipeline import RecommendationRankingPipeline
from ai.search.parser import QueryIntentParser
from ai.forecasting.forecaster import DemandForecaster
from ai.fraud.detector import fraud_detector
from ai.segmentation.segmenter import CustomerSegmenter
from ai.churn.predictor import ChurnPredictor
from ai.model_registry.registry import ModelRegistryService
from ai.shopping_agent.agent import AIShoppingAgent
from ai.shopping_agent.memory import SessionMemoryRegistry
from ai.shopping_agent.analytics import ConversationAnalytics

router = APIRouter(prefix="/ai", tags=["AI & Machine Learning"])



@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    strategy: str = Query("HYBRID", description="POPULARITY, CONTENT, COLLABORATIVE, HYBRID, NEURAL"),
    product_id: Optional[int] = Query(None, description="Optional seed product ID for content-based similarity"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Retrieve personalized product recommendations powered by multi-level AI models."""
    user_id = current_user.id if current_user else None
    all_products = db.query(Product).filter(Product.is_active == True).all()
    if not all_products:
        return RecommendationResponse(user_id=user_id, strategy=strategy, recommendations=[])

    prod_map = {p.id: p for p in all_products}
    items: List[RecommendationItem] = []

    if strategy.upper() == "POPULARITY":
        recs = recommender_engine.get_popularity_recommendations(all_products, limit=limit)
        for pid, score, expl in recs:
            if pid in prod_map:
                items.append(RecommendationItem(product=ProductRead.model_validate(prod_map[pid]), score=score, explanation=expl, model_type="POPULARITY"))

    elif strategy.upper() == "CONTENT" and product_id:
        recs = recommender_engine.get_content_recommendations(product_id, limit=limit)
        for pid, score, expl in recs:
            if pid in prod_map:
                items.append(RecommendationItem(product=ProductRead.model_validate(prod_map[pid]), score=score, explanation=expl, model_type="CONTENT"))

    elif strategy.upper() == "COLLABORATIVE" and user_id:
        recs = recommender_engine.get_collaborative_recommendations(user_id, limit=limit)
        for pid, score, expl in recs:
            if pid in prod_map:
                items.append(RecommendationItem(product=ProductRead.model_validate(prod_map[pid]), score=score, explanation=expl, model_type="COLLABORATIVE"))

    elif strategy.upper() == "NEURAL" and user_id:
        recs = recommender_engine.get_matrix_factorization_recommendations(user_id, all_products, limit=limit)
        for pid, score, expl in recs:
            if pid in prod_map:
                items.append(RecommendationItem(product=ProductRead.model_validate(prod_map[pid]), score=score, explanation=expl, model_type="NEURAL"))

    else:  # Default HYBRID
        recs = recommender_engine.get_hybrid_recommendations(user_id, all_products, recent_product_id=product_id, limit=limit)
        for pid, score, expl, m_type in recs:
            if pid in prod_map:
                items.append(RecommendationItem(product=ProductRead.model_validate(prod_map[pid]), score=score, explanation=expl, model_type=m_type))

    return RecommendationResponse(user_id=user_id, strategy=strategy, recommendations=items)


@router.get("/recommendations/pipeline")
def get_recommendation_pipeline(
    category_id: Optional[int] = Query(None, description="Optional category filter"),
    diversity: float = Query(0.7, ge=0.1, le=1.0, description="MMR diversity trade-off factor"),
    limit: int = Query(10, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Executes full multi-stage ranking pipeline with MMR diversity adjustment."""
    user_id = current_user.id if current_user else None
    return RecommendationRankingPipeline.rank_for_user(
        db=db,
        user_id=user_id,
        limit=limit,
        category_id=category_id,
        diversity_lambda=diversity
    )


@router.get("/recommendations/session")
def get_session_recommendations(
    viewed_ids: str = Query("", description="Comma-separated product IDs in current session"),
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Generates real-time session-based recommendations from active session browsing sequence."""
    ids = [int(x.strip()) for x in viewed_ids.split(",") if x.strip().isdigit()]
    return RecommendationRankingPipeline.rank_for_session(
        db=db,
        viewed_product_ids=ids,
        limit=limit
    )


@router.post("/search/parse-intent", response_model=ParsedSearchIntent)
def parse_search_intent(query_text: str = Query(..., description="Natural language search query")):
    """Convert conversational user search query into structured constraints."""
    parsed = QueryIntentParser.parse_query(query_text)
    return ParsedSearchIntent(**parsed)


@router.get("/forecast/product/{product_id}", response_model=DemandForecastItem)
def get_product_demand_forecast(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Generate time-series future demand forecast and stock reorder intelligence from real sales history."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Product", str(product_id))

    # Fetch real order item dates and quantities
    order_items = db.query(OrderItem.created_at, OrderItem.quantity).filter(
        OrderItem.product_id == product_id
    ).all()

    sales_history = [{"date": oi.created_at, "quantity": oi.quantity} for oi in order_items]

    forecast = DemandForecaster.train_and_forecast(
        sales_history=sales_history,
        current_stock=product.stock,
        lead_time_days=5
    )

    return DemandForecastItem(
        product_id=product.id,
        product_name=product.name,
        current_stock=product.stock,
        predicted_demand_next_7_days=forecast["predicted_demand_next_7_days"],
        predicted_demand_next_30_days=forecast["predicted_demand_next_30_days"],
        reorder_recommended=forecast["reorder_recommended"],
        recommended_reorder_units=forecast["recommended_reorder_units"],
        model_algorithm=forecast["algorithm"],
        confidence_score=forecast["confidence_score"],
        evaluation_metrics=forecast["evaluation_metrics"]
    )


@router.get("/fraud/order/{order_id}", response_model=FraudRiskEvaluation)
def evaluate_order_fraud(
    order_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Run Isolation Forest anomaly scoring on an order transaction."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Order", str(order_id))

    user = order.customer
    user_orders = db.query(Order).filter(Order.customer_id == user.id).all()
    user_avg = float(np.mean([o.total_amount for o in user_orders])) if user_orders else order.total_amount
    days_old = max(1, (datetime.now(timezone.utc) - user.created_at.replace(tzinfo=timezone.utc)).days)
    items_count = sum(i.quantity for i in order.items)

    risk_eval = fraud_detector.evaluate_transaction(
        order_amount=order.total_amount,
        items_count=items_count,
        days_since_signup=days_old,
        past_orders_count=len(user_orders),
        failed_attempts_24h=0,
        user_avg_order_amount=user_avg
    )

    # Save to fraud alerts table if suspicious
    if risk_eval["is_suspicious"]:
        existing = db.query(FraudAlert).filter(FraudAlert.order_id == order.id).first()
        if not existing:
            alert = FraudAlert(
                order_id=order.id,
                user_id=user.id,
                risk_score=risk_eval["risk_score"],
                risk_level=risk_eval["risk_level"],
                trigger_reasons=risk_eval["trigger_reasons"],
                status="PENDING_REVIEW"
            )
            db.add(alert)
            db.commit()

    return FraudRiskEvaluation(
        order_id=order.id,
        risk_score=risk_eval["risk_score"],
        risk_level=risk_eval["risk_level"],
        is_suspicious=risk_eval["is_suspicious"],
        trigger_reasons=risk_eval["trigger_reasons"],
        suggested_action=risk_eval["suggested_action"]
    )


@router.get("/segmentation/customer/{user_id}", response_model=CustomerSegmentProfile)
def get_customer_segment(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))
):
    """Retrieve customer RFM behavioral segment computed via K-Means."""
    orders = db.query(Order).filter(Order.customer_id == user_id, Order.status != "CANCELLED").all()
    total_spend = sum(o.total_amount for o in orders)
    freq = len(orders)
    now = datetime.now(timezone.utc)
    recency = (now - max((o.created_at.replace(tzinfo=timezone.utc) for o in orders), default=now)).days if orders else 90

    rfm_data = [{"user_id": user_id, "recency_days": recency, "frequency": freq, "monetary": total_spend}]
    cluster_res = CustomerSegmenter.cluster_customers(rfm_data)
    seg_info = cluster_res["segments"][0]

    return CustomerSegmentProfile(
        user_id=user_id,
        segment_name=seg_info["segment_name"],
        recency_days=seg_info["recency_days"],
        order_frequency=seg_info["order_frequency"],
        total_monetary_spend=seg_info["total_monetary_spend"],
        silhouette_score=cluster_res["silhouette_score"],
        description=seg_info["description"]
    )


@router.get("/churn/customer/{user_id}", response_model=ChurnRiskProfile)
def predict_customer_churn(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))
):
    """Predict customer churn probability and identify retention triggers."""
    orders = db.query(Order).filter(Order.customer_id == user_id).all()
    now = datetime.now(timezone.utc)
    recency_days = (now - max((o.created_at.replace(tzinfo=timezone.utc) for o in orders), default=now)).days if orders else 60
    reviews_count = db.query(Review).filter(Review.user_id == user_id).count()

    churn_res = ChurnPredictor.evaluate_churn_risk(
        days_since_last_purchase=recency_days,
        total_orders=len(orders),
        days_since_last_login=min(30, recency_days // 2),
        cart_abandonment_count=1 if not orders else 0,
        reviews_count=reviews_count,
        wishlist_count=1
    )

    return ChurnRiskProfile(
        user_id=user_id,
        churn_probability=churn_res["churn_probability"],
        risk_category=churn_res["risk_category"],
        contributing_factors=churn_res["contributing_factors"],
        suggested_retention_action=churn_res["suggested_retention_action"]
    )


@router.post("/assistant/chat", response_model=ShoppingAssistantResponse)
def ai_shopping_assistant(
    request: ShoppingAssistantRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Conversational AI Shopping Assistant grounded in actual catalog products.
    Performs requirement extraction, tool execution, comparison tables, cart actions, and multi-turn session memory.
    """
    user_id = current_user.id if current_user else request.user_id

    res = AIShoppingAgent.process_message(
        db=db,
        message=request.user_message,
        user_id=user_id,
        context=request.context,
        session_id=request.session_id
    )

    # Format grounded products
    grounded = []
    for p_card in res.get("recommended_products", []):
        if "id" in p_card:
            p_obj = db.query(Product).filter(Product.id == p_card["id"]).first()
            if p_obj:
                grounded.append(ProductRead.model_validate(p_obj))

    # Backward compatibility parsed intent
    parsed = QueryIntentParser.parse_query(request.user_message)

    return ShoppingAssistantResponse(
        assistant_reply=res.get("reply_text") or res.get("reply", ""),
        parsed_intent=ParsedSearchIntent(**parsed),
        grounded_products=grounded,
        confidence_score=res.get("evaluation", {}).get("groundedness_score", 0.95),
        reasoning=f"Agent intent: {res.get('intent', 'DISCOVERY')}. Tools: {', '.join(res.get('tools_invoked', []))}",
        session_id=res.get("session_id"),
        intent=res.get("intent"),
        action_pills=res.get("action_pills", []),
        comparison_table=res.get("comparison_table"),
        cart_result=res.get("cart_result"),
        order_result=res.get("order_result"),
        bundle=res.get("bundle"),
        extracted_requirements=res.get("extracted_requirements"),
        evaluation=res.get("evaluation")
    )


@router.get("/shopping-agent/history/{session_id}")
def get_shopping_agent_history(session_id: str):
    """Retrieve multi-turn dialogue memory and extracted preferences for a session."""
    mem = SessionMemoryRegistry.get_session(session_id)
    if not mem:
        return {"session_id": session_id, "turns": [], "cumulative_preferences": {}}
    return mem.to_dict()


@router.post("/shopping-agent/feedback")
def submit_shopping_agent_feedback(payload: dict):
    """Submit user feedback (thumbs up / thumbs down) for an agent interaction."""
    is_positive = bool(payload.get("is_positive", True))
    session_id = payload.get("session_id", "default")
    turn_index = int(payload.get("turn_index", 0))
    ConversationAnalytics.record_feedback(is_positive=is_positive, session_id=session_id, turn_index=turn_index)
    return {"success": True, "message": "Feedback recorded for model evaluation."}


@router.get("/shopping-agent/analytics")
def get_shopping_agent_analytics(admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))):
    """Retrieve real-time conversation telemetry, intent distribution, tool metrics, and failure diagnostics."""
    return ConversationAnalytics.get_summary()


@router.get("/model-registry")
def list_registered_models(db: Session = Depends(get_db)):
    """List all AI models, versions, algorithms, and real evaluation metrics."""
    return ModelRegistryService.list_models(db)

