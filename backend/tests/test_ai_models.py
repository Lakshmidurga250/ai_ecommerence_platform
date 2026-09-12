"""
Artificial Intelligence & Machine Learning Automated Test Suite.
Validates that recommendation, sentiment, forecasting, fraud, segmentation,
and churn models calculate real mathematical outputs (no hardcoded data).
"""

from ai.sentiment.analyzer import SentimentAnalyzer
from ai.search.parser import QueryIntentParser
from ai.forecasting.forecaster import DemandForecaster
from ai.fraud.detector import fraud_detector
from ai.segmentation.segmenter import CustomerSegmenter
from ai.churn.predictor import ChurnPredictor


def test_sentiment_analyzer():
    # Positive test
    pos_res = SentimentAnalyzer.analyze_text("This laptop is absolutely amazing! Outstanding battery life and build quality.")
    assert pos_res["sentiment_label"] == "POSITIVE"
    assert pos_res["polarity_score"] > 0.4
    assert pos_res["confidence_score"] > 0.7
    assert "battery" in pos_res["extracted_aspects"] or "quality" in pos_res["extracted_aspects"]

    # Negative test
    neg_res = SentimentAnalyzer.analyze_text("Terrible experience. The shoes were broken and very uncomfortable. Worst purchase!")
    assert neg_res["sentiment_label"] == "NEGATIVE"
    assert neg_res["polarity_score"] < -0.4

    # Neutral test
    neu_res = SentimentAnalyzer.analyze_text("The item was delivered in a standard brown box.")
    assert neu_res["sentiment_label"] == "NEUTRAL"
    assert abs(neu_res["polarity_score"]) < 0.2


def test_query_intent_parser():
    parsed = QueryIntentParser.parse_query("comfortable black running shoes under 4000 with 4 star rating")
    assert parsed["extracted_color"] == "black"
    assert parsed["extracted_category"] == "running shoes"
    assert parsed["max_price"] == 4000.0
    assert parsed["min_rating"] == 4.0
    assert parsed["is_semantic_intent"] is True


def test_demand_forecaster():
    # Synthetic time-series history
    from datetime import datetime, timedelta
    base_date = datetime.now() - timedelta(days=30)
    sales_history = [
        {"date": (base_date + timedelta(days=i)).isoformat(), "quantity": 3 + (i % 4)}
        for i in range(30)
    ]
    res = DemandForecaster.train_and_forecast(sales_history, current_stock=20)
    assert "predicted_demand_next_7_days" in res
    assert "predicted_demand_next_30_days" in res
    assert res["predicted_demand_next_7_days"] > 0
    assert res["predicted_demand_next_30_days"] > res["predicted_demand_next_7_days"]
    assert "mae" in res["evaluation_metrics"]
    assert "rmse" in res["evaluation_metrics"]
    assert "mape" in res["evaluation_metrics"]
    assert res["evaluation_metrics"]["mae"] >= 0.0


def test_fraud_anomaly_detector():
    # Normal transaction
    normal_res = fraud_detector.evaluate_transaction(
        order_amount=2400.0,
        items_count=2,
        days_since_signup=90,
        past_orders_count=8,
        failed_attempts_24h=0,
        user_avg_order_amount=2200.0
    )
    assert normal_res["risk_score"] < 50.0
    assert normal_res["is_suspicious"] is False

    # Highly anomalous transaction
    anom_res = fraud_detector.evaluate_transaction(
        order_amount=85000.0,
        items_count=20,
        days_since_signup=1,
        past_orders_count=0,
        failed_attempts_24h=4,
        user_avg_order_amount=2000.0
    )
    assert anom_res["risk_score"] >= 55.0
    assert anom_res["is_suspicious"] is True
    assert len(anom_res["trigger_reasons"]) >= 2


def test_customer_rfm_segmenter():
    customers_rfm = [
        {"user_id": 1, "recency_days": 5, "frequency": 12, "monetary": 85000.0},
        {"user_id": 2, "recency_days": 10, "frequency": 8, "monetary": 42000.0},
        {"user_id": 3, "recency_days": 75, "frequency": 1, "monetary": 1200.0},
        {"user_id": 4, "recency_days": 90, "frequency": 2, "monetary": 2500.0},
        {"user_id": 5, "recency_days": 15, "frequency": 5, "monetary": 15000.0}
    ]
    res = CustomerSegmenter.cluster_customers(customers_rfm)
    assert "silhouette_score" in res
    assert len(res["segments"]) == 5
    assert all("segment_name" in s for s in res["segments"])


def test_churn_predictor():
    active_user = ChurnPredictor.evaluate_churn_risk(
        days_since_last_purchase=5,
        total_orders=10,
        days_since_last_login=2,
        cart_abandonment_count=0,
        reviews_count=4,
        wishlist_count=3
    )
    assert active_user["churn_probability"] < 0.35
    assert active_user["risk_category"] == "LOW"

    dormant_user = ChurnPredictor.evaluate_churn_risk(
        days_since_last_purchase=120,
        total_orders=1,
        days_since_last_login=45,
        cart_abandonment_count=4,
        reviews_count=0,
        wishlist_count=0
    )
    assert dormant_user["churn_probability"] > 0.60
    assert dormant_user["risk_category"] in ("HIGH", "MEDIUM")


def test_recommendation_api_endpoints(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    
    # Hybrid recs
    res_hybrid = client.get("/api/v1/ai/recommendations?strategy=HYBRID", headers=headers)
    assert res_hybrid.status_code == 200
    assert len(res_hybrid.json()["recommendations"]) > 0

    # Popularity recs
    res_pop = client.get("/api/v1/ai/recommendations?strategy=POPULARITY")
    assert res_pop.status_code == 200
    assert len(res_pop.json()["recommendations"]) > 0

    # Assistant chat grounded retrieval
    chat_res = client.post("/api/v1/ai/assistant/chat", json={
        "user_message": "Looking for black shoes under 10000"
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert len(chat_data["grounded_products"]) > 0
    assert chat_data["confidence_score"] > 0.70
