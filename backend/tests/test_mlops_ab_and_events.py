"""
Tests for MLOps Model Registry, Statistical Drift Monitoring, A/B Testing, Event Tracking, and Loyalty Engine.
"""

import pytest
from ai.model_registry.mlops_service import MLOpsService
from app.services.ab_testing_service import ABTestingService
from app.services.loyalty_service import LoyaltyService


@pytest.fixture
def mlops_service(db_session):
    return MLOpsService(db_session)


@pytest.fixture
def ab_service(db_session):
    return ABTestingService(db_session)


@pytest.fixture
def loyalty_service(db_session):
    return LoyaltyService(db_session)


def test_mlops_service_init(mlops_service):
    """Verify MLOpsService instantiation."""
    assert mlops_service is not None
    assert hasattr(mlops_service, "get_models")
    assert hasattr(mlops_service, "get_drift_logs")
    assert hasattr(mlops_service, "promote_model")


def test_mlops_model_registry_list(mlops_service):
    """Verify registered AI models have version, stage, and accuracy metrics."""
    models = mlops_service.get_models()
    assert isinstance(models, list)
    assert len(models) >= 5
    for m in models:
        assert "model_name" in m
        assert "version" in m
        assert "stage" in m
        assert "accuracy_metric" in m


def test_mlops_model_promotion(mlops_service):
    """Verify promoting a model changes its stage."""
    models = mlops_service.get_models()
    first_id = models[0]["model_id"]
    res = mlops_service.promote_model(first_id, "PRODUCTION")
    assert res["stage"] == "PRODUCTION"


def test_mlops_drift_monitoring(mlops_service):
    """Verify statistical drift records contain p-values and baseline comparison."""
    drift = mlops_service.get_drift_logs()
    assert isinstance(drift, list)
    assert len(drift) > 0
    first = drift[0]
    assert "model_name" in first
    assert "drift_metric" in first
    assert "p_value" in first
    assert isinstance(first["drift_detected"], bool)


def test_mlops_models_api_endpoint(client, admin_token):
    """Verify GET /api/v1/mlops/models."""
    res = client.get(
        "/api/v1/mlops/models",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 5


def test_mlops_drift_api_endpoint(client, admin_token):
    """Verify GET /api/v1/mlops/drift."""
    res = client.get(
        "/api/v1/mlops/drift",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_ab_testing_service_init(ab_service):
    """Verify ABTestingService instantiation."""
    assert ab_service is not None
    assert hasattr(ab_service, "get_experiments")
    assert hasattr(ab_service, "get_experiment_analytics")


def test_ab_testing_analytics_calculation(ab_service):
    """Verify A/B conversion rate and relative lift calculation."""
    exps = ab_service.get_experiments()
    assert len(exps) > 0
    exp_id = exps[0]["experiment_id"]
    analytics = ab_service.get_experiment_analytics(exp_id)
    assert "variants" in analytics
    assert len(analytics["variants"]) >= 2
    for v in analytics["variants"]:
        assert "conversion_rate" in v
        assert "lift_pct" in v


def test_experiments_api_endpoints(client):
    """Verify GET /api/v1/experiments/ and analytics endpoint."""
    res = client.get("/api/v1/experiments/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0

    exp_id = data[0]["experiment_id"]
    res_analytics = client.get(f"/api/v1/experiments/{exp_id}/analytics")
    assert res_analytics.status_code == 200
    data_analytics = res_analytics.json()
    assert "variants" in data_analytics


def test_event_tracking_single_endpoint(client):
    """Verify POST /api/v1/events/track."""
    res = client.post(
        "/api/v1/events/track",
        json={
            "event_type": "PRODUCT_VIEW",
            "product_id": 1,
            "page_url": "/product/1",
            "metadata": {"source": "recommendation_rail"}
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "RECORDED"


def test_event_tracking_batch_endpoint(client):
    """Verify POST /api/v1/events/batch."""
    res = client.post(
        "/api/v1/events/batch",
        json={
            "events": [
                {"event_type": "PAGE_VIEW", "page_url": "/"},
                {"event_type": "SEARCH", "metadata": {"query": "running shoes"}}
            ]
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["processed_count"] == 2


def test_event_summary_endpoint(client, admin_token):
    """Verify GET /api/v1/events/summary."""
    res = client.get(
        "/api/v1/events/summary",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "total_events" in data
    assert "breakdown" in data


def test_loyalty_service_profile(loyalty_service):
    """Verify loyalty profile computation."""
    profile = loyalty_service.get_loyalty_profile(user_id=1)
    assert profile is not None
    assert "current_points" in profile
    assert "tier" in profile
    assert profile["tier"] in ["BRONZE", "SILVER", "GOLD", "PLATINUM"]


def test_loyalty_api_endpoints(client, customer_token):
    """Verify GET /api/v1/loyalty/me and POST /api/v1/loyalty/redeem."""
    res = client.get(
        "/api/v1/loyalty/me",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "current_points" in data
    assert "tier" in data

    # Test redemption
    redeem_res = client.post(
        "/api/v1/loyalty/redeem",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={"points": 50}
    )
    assert redeem_res.status_code in [200, 400]
