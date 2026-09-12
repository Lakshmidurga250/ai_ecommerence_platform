"""
Test suite validating AI engines, models, and predictive pipelines.
"""

import pytest
from ai.churn.predictor import ChurnPredictor
from ai.forecasting.forecaster import DemandForecaster
from ai.sentiment.analyzer import SentimentAnalyzer
from ai.shopping_agent.agent import AIShoppingAgent

def test_churn_predictor_inference():
    """Validate customer churn prediction model output."""
    result = ChurnPredictor.evaluate_churn_risk(
        days_since_last_purchase=45,
        total_orders=3,
        days_since_last_login=10,
        cart_abandonment_count=2,
        reviews_count=2,
        wishlist_count=4,
    )
    assert "churn_probability" in result
    assert 0.0 <= result["churn_probability"] <= 1.0

def test_demand_forecaster_inference():
    """Validate demand forecasting inference."""
    dummy_series = [{"date": f"2026-08-{i:02d}", "quantity": (i % 5) + 1} for i in range(1, 20)]
    forecast = DemandForecaster.train_and_forecast(dummy_series, current_stock=20, lead_time_days=3)
    assert "predicted_demand_next_7_days" in forecast or "algorithm" in forecast

def test_sentiment_analyzer():
    """Validate sentiment scoring."""
    res = SentimentAnalyzer.analyze_text("This product is fantastic and exceeds all expectations!")
    assert "sentiment_label" in res
    assert res["sentiment_label"] in ("POSITIVE", "NEUTRAL", "NEGATIVE")

def test_shopping_agent_initialization():
    """Validate conversational AI shopping agent instance."""
    agent = AIShoppingAgent()
    assert agent is not None
