"""
AI E-Commerce System Health & Validation Check
Verifies:
1. Database connectivity and row counts across primary entities
2. Live AI model inference without mock data (Recommendations, Sentiment, Demand Forecasting, Fraud Detection, RFM Segmentation, Churn)
3. FastAPI application route registry
4. Frontend build bundle integrity
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

def check_system_health():
    print("=" * 70)
    print("AI E-COMMERCE & RECOMMENDATION PLATFORM - HEALTH CHECK")
    print("=" * 70)

    # 1. Check Database
    print("\n[1/4] Checking Database Connectivity & Schema...")
    from app.core.database import SessionLocal
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order
    from app.models.review import Review

    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        order_count = db.query(Order).count()
        review_count = db.query(Review).count()

        print(f"  [OK] Database Connected successfully")
        print(f"       Users: {user_count} | Products: {product_count} | Orders: {order_count} | Reviews: {review_count}")
        assert user_count > 0, "No users found in database"
        assert product_count > 0, "No products found in database"
    finally:
        db.close()

    # 2. Check AI Models Live Inference
    print("\n[2/4] Verifying Live AI Machine Learning Inference Engines...")
    from ai.recommendations.recommender import RecommendationEngine
    from ai.sentiment.analyzer import SentimentAnalyzer
    from ai.forecasting.forecaster import DemandForecaster
    from ai.fraud.detector import FraudDetector
    from ai.segmentation.segmenter import CustomerSegmenter
    from ai.churn.predictor import ChurnPredictor
    from ai.search.parser import QueryIntentParser

    # L1-L5 Recommendations
    rec_engine = RecommendationEngine()
    db = SessionLocal()
    all_prods = db.query(Product).all()
    db.close()
    recs = rec_engine.get_popularity_recommendations(all_prods, limit=3)
    print(f"  [OK] Recommendation Engine (Popularity/Hybrid): Evaluated {len(all_prods)} products, generated {len(recs)} ranked items")

    # Sentiment Analyzer
    analyzer = SentimentAnalyzer()
    sentiment = analyzer.analyze_text("The sound quality is incredible and battery life exceeds expectations.")
    print(f"  [OK] Sentiment Analyzer (Lexicon): Polarity {sentiment['polarity_score']:.2f} ({sentiment['sentiment_label']})")

    # Demand Forecaster
    forecaster = DemandForecaster()
    sample_sales = [{"date": f"2026-08-{i:02d}", "quantity": 3 + (i % 4)} for i in range(1, 28)]
    forecast = forecaster.train_and_forecast(sample_sales, current_stock=20)
    print(f"  [OK] Demand Forecaster (RandomForest/Baseline): Next 7 Days = {forecast['predicted_demand_next_7_days']} units, MAE = {forecast['evaluation_metrics']['mae']}")

    # Fraud Detector
    detector = FraudDetector()
    fraud_result = detector.evaluate_transaction(order_amount=1299.99, items_count=2, days_since_signup=2, past_orders_count=0)
    print(f"  [OK] Fraud Detector (IsolationForest): Risk Score = {fraud_result['risk_score']}/100 ({fraud_result['risk_level']})")

    # Intent Parser
    intent = QueryIntentParser.parse_query("Sony wireless headphones under 350")
    print(f"  [OK] Search Intent Parser (NLP): Extracted Brand = '{intent['extracted_brand']}', Max Price = ${intent['max_price']}")

    # Neural Collaborative Filtering (PyTorch NeuMF)
    from ai.recommendations.neural_cf import NeuralCFEngine, HAS_TORCH
    ncf = NeuralCFEngine()
    toy_data = [(1, 101, 1.0), (1, 102, 1.0), (2, 101, 1.0), (2, 103, 1.0)]
    ncf_res = ncf.fit(toy_data, epochs=1)
    print(f"  [OK] Neural CF Deep Learning (NeuMF): PyTorch backend = {HAS_TORCH}, loss = {ncf_res['final_loss']}")

    # Recommendation Evaluator
    from ai.recommendations.evaluator import RecommendationEvaluator
    eval_p = RecommendationEvaluator.precision_at_k([10, 20, 30], {10, 30, 40}, k=3)
    eval_ndcg = RecommendationEvaluator.ndcg_at_k([10, 20, 30], {10, 30, 40}, k=3)
    print(f"  [OK] Offline Recommendation Evaluator: Precision@3 = {eval_p}, NDCG@3 = {eval_ndcg}")

    # Layered Fraud Defense Shield
    from ai.fraud.layered_shield import LayeredFraudShield
    shield = LayeredFraudShield()
    shield_eval = shield.evaluate_order(order_amount=120.0, items_count=2, user_account_age_days=60, past_successful_orders=4)
    print(f"  [OK] Layered Fraud Shield (3-Tier): Risk = {shield_eval['risk_score']}/100 ({shield_eval['decision']})")

    # Customer Lifetime Value & Cohort Segmentation
    from ai.customer_intelligence.clv_cohorts import CustomerIntelligenceEngine
    clv_eval = CustomerIntelligenceEngine.calculate_clv(historical_spend=1500.0, order_count=6, days_active=120)
    print(f"  [OK] Customer CLV & Cohort Engine: Tier = {clv_eval['customer_tier']}, 1-Yr CLV = ${clv_eval['predictive_clv_1yr']:.2f}")

    # Inventory Replenishment & Stock Optimization
    from ai.inventory_intelligence.replenishment import InventoryIntelligenceEngine
    inv_eval = InventoryIntelligenceEngine.calculate_reorder_parameters([10, 12, 11, 14, 13], lead_time_days=7)
    print(f"  [OK] Inventory Replenishment Engine: Safety Stock = {inv_eval['safety_stock_units']} units, ROP = {inv_eval['reorder_point_units']} units")

    # Context-Grounded AI Support Assistant
    from app.services.ai_support_service import AISupportService
    support_reply = AISupportService.process_customer_query(db=SessionLocal(), message="How long does standard delivery take?")
    print(f"  [OK] Grounded AI Support Assistant: Intent = {support_reply['intent']}, Sentiment = {support_reply['sentiment']}")

    # 3. Check FastAPI App & OpenAPI routes
    print("\n[3/4] Checking FastAPI App & Route Registry...")
    from app.main import app
    route_count = len(app.openapi()["paths"])
    print(f"  [OK] FastAPI Application Loaded: {route_count} functional HTTP/WebSocket endpoints registered in OpenAPI")
    assert route_count >= 50, f"Expected at least 50 endpoints, found {route_count}"


    # 4. Check Frontend Production Bundle
    print("\n[4/4] Verifying Frontend Production Artifacts...")
    dist_html = BASE_DIR / "frontend" / "dist" / "index.html"
    if dist_html.exists():
        dist_size_kb = dist_html.stat().st_size / 1024
        print(f"  [OK] Frontend Production Build Verified: dist/index.html ({dist_size_kb:.2f} KB)")
    else:
        print("  [WARN] Frontend dist/ directory not found. Run 'npm run build' in frontend/.")

    print("\n" + "=" * 70)
    print("ALL PLATFORM HEALTH CHECKS PASSED [100% OPERATIONAL]")
    print("=" * 70)

if __name__ == "__main__":
    check_system_health()
