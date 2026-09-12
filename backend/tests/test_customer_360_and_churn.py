"""
Tests for Customer 360, Churn Modeling, Predictive CLV, and Review Intelligence.
Validates RFM segmentation, customer lifetime value, retention playbooks, and sentiment aspect breakdown.
"""

import pytest
from app.services.customer_360_service import Customer360Service
from ai.sentiment.review_intelligence import ReviewIntelligenceService


@pytest.fixture
def c360_service(db_session):
    return Customer360Service(db_session)


@pytest.fixture
def review_intel_service(db_session):
    return ReviewIntelligenceService(db_session)


def test_customer_360_service_init(c360_service):
    """Verify service instantiation."""
    assert c360_service is not None
    assert hasattr(c360_service, "get_customer_360")


def test_customer_360_profile_generation(c360_service):
    """Verify Customer 360 profile contains RFM, CLV, and churn metrics."""
    profile = c360_service.get_customer_360(user_id=1)
    assert profile is not None
    assert "summary" in profile
    assert "rfm" in profile
    assert "predictive_metrics" in profile
    assert "preferences" in profile
    assert "retention_recommendations" in profile


def test_rfm_metrics_accuracy(c360_service):
    """Verify RFM values are non-negative and properly computed."""
    profile = c360_service.get_customer_360(user_id=1)
    rfm = profile["rfm"]
    assert rfm["recency_days"] >= 0
    assert rfm["frequency_orders"] >= 0
    assert rfm["monetary_spend"] >= 0.0
    assert rfm["aov"] >= 0.0
    assert isinstance(rfm["rfm_segment"], str)


def test_churn_probability_bounds(c360_service):
    """Verify churn probability is bounded between 0 and 1."""
    profile = c360_service.get_customer_360(user_id=1)
    churn = profile["predictive_metrics"]["churn_probability"]
    assert 0.0 <= churn <= 1.0
    assert profile["predictive_metrics"]["churn_risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_predicted_clv_positive(c360_service):
    """Verify predictive CLV is greater than zero."""
    profile = c360_service.get_customer_360(user_id=1)
    clv = profile["predictive_metrics"]["predicted_clv"]
    assert clv >= 0.0


def test_customer_preferences_structure(c360_service):
    """Verify category and brand affinities are extracted."""
    profile = c360_service.get_customer_360(user_id=1)
    prefs = profile["preferences"]
    assert "favorite_categories" in prefs
    assert "favorite_brands" in prefs
    assert isinstance(prefs["favorite_categories"], list)


def test_retention_recommendations_actionable(c360_service):
    """Verify retention recommendations include urgency and channel."""
    profile = c360_service.get_customer_360(user_id=1)
    recs = profile["retention_recommendations"]
    assert len(recs) > 0
    for r in recs:
        assert "action" in r
        assert "channel" in r
        assert "urgency" in r
        assert r["urgency"] in ["LOW", "MEDIUM", "HIGH"]


def test_customer_360_me_endpoint(client, customer_token):
    """Verify GET /api/v1/customer-intelligence/me/360."""
    res = client.get(
        "/api/v1/customer-intelligence/me/360",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "user_id" in data
    assert "rfm" in data
    assert "predictive_metrics" in data


def test_customer_360_admin_endpoint(client, admin_token):
    """Verify GET /api/v1/customer-intelligence/users/{id}/360."""
    res = client.get(
        "/api/v1/customer-intelligence/users/1/360",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == 1


def test_customer_360_unauthorized(client):
    """Verify 401 when token is missing."""
    res = client.get("/api/v1/customer-intelligence/me/360")
    assert res.status_code == 401


def test_review_intelligence_service(review_intel_service):
    """Verify ReviewIntelligenceService synthesizes aspect ratings."""
    summary = review_intel_service.generate_product_intelligence(product_id=1)
    assert summary is not None
    assert "authenticity_score" in summary
    assert "aspect_breakdown" in summary
    assert "consensus_summary" in summary
    assert 0.0 <= summary["authenticity_score"] <= 1.0


def test_review_intelligence_api_endpoint(client):
    """Verify GET /api/v1/reviews/product/{id}/intelligence-summary."""
    res = client.get("/api/v1/reviews/product/1/intelligence-summary")
    assert res.status_code == 200
    data = res.json()
    assert "aspect_breakdown" in data
    assert "top_pros" in data
    assert "top_cons" in data
    assert "authenticity_score" in data
