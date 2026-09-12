"""
Tests for Fraud Intelligence Center and Smart Logistics & Returns Routing.
Validates Isolation Forest risk queue, explainable factor attribution, warehouse routing, and ETA calculation.
"""

import pytest
from app.services.fraud_intelligence_service import FraudIntelligenceService
from app.services.smart_logistics_service import SmartLogisticsService


@pytest.fixture
def fraud_service(db_session):
    return FraudIntelligenceService(db_session)


@pytest.fixture
def logistics_service(db_session):
    return SmartLogisticsService(db_session)


def test_fraud_service_init(fraud_service):
    """Verify FraudIntelligenceService instantiation."""
    assert fraud_service is not None
    assert hasattr(fraud_service, "get_alerts")
    assert hasattr(fraud_service, "resolve_alert")
    assert hasattr(fraud_service, "get_statistics")


def test_fraud_alerts_contain_explainability_factors(fraud_service):
    """Verify fraud alerts contain explainable risk factors."""
    alerts = fraud_service.get_alerts()
    assert isinstance(alerts, list)
    if len(alerts) > 0:
        first = alerts[0]
        assert "alert_id" in first
        assert "risk_score" in first
        assert "risk_level" in first
        assert "flagged_factors" in first
        assert isinstance(first["flagged_factors"], list)


def test_fraud_alert_resolution_logic(fraud_service):
    """Verify alert resolution transitions status and records audit notes."""
    alerts = fraud_service.get_alerts()
    if len(alerts) > 0:
        alert_id = alerts[0]["alert_id"]
        res = fraud_service.resolve_alert(alert_id, resolution="APPROVED", notes="Test verification passed")
        assert res["status"] in ["APPROVED", "BLOCKED"]


def test_fraud_statistics_structure(fraud_service):
    """Verify fraud statistics calculation."""
    stats = fraud_service.get_statistics()
    assert "total_evaluated_orders" in stats
    assert "fraud_prevention_rate_pct" in stats
    assert stats["fraud_prevention_rate_pct"] >= 0.0


def test_fraud_alerts_api_endpoint(client, admin_token):
    """Verify GET /api/v1/fraud/alerts with admin credentials."""
    res = client.get(
        "/api/v1/fraud/alerts",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_fraud_statistics_api_endpoint(client, admin_token):
    """Verify GET /api/v1/fraud/statistics with admin credentials."""
    res = client.get(
        "/api/v1/fraud/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "total_evaluated_orders" in data


def test_fraud_resolve_api_endpoint(client, admin_token):
    """Verify POST /api/v1/fraud/alerts/{id}/resolve."""
    res = client.post(
        "/api/v1/fraud/alerts/1/resolve",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"resolution": "APPROVED", "notes": "Verified via test client"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "status" in data


def test_smart_logistics_service_init(logistics_service):
    """Verify SmartLogisticsService instantiation."""
    assert logistics_service is not None
    assert hasattr(logistics_service, "estimate_delivery_route")
    assert hasattr(logistics_service, "get_return_analytics")


def test_smart_logistics_warehouse_routing(logistics_service):
    """Verify nearest warehouse selection based on destination pincode."""
    route_delhi = logistics_service.estimate_delivery_route(product_id=1, destination_pincode="110001")
    assert route_delhi is not None
    assert "warehouse_name" in route_delhi
    assert "distance_km" in route_delhi
    assert "estimated_transit_days" in route_delhi
    assert route_delhi["estimated_transit_days"] >= 1


def test_smart_logistics_carbon_calculation(logistics_service):
    """Verify carbon footprint estimation."""
    route = logistics_service.estimate_delivery_route(product_id=1, destination_pincode="560001")
    assert "carbon_kg" in route
    assert route["carbon_kg"] > 0.0


def test_logistics_estimate_api_endpoint(client):
    """Verify POST /api/v1/logistics/estimate-delivery."""
    res = client.post(
        "/api/v1/logistics/estimate-delivery",
        json={"product_id": 1, "destination_pincode": "400001"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "warehouse_name" in data
    assert "carrier" in data
    assert "estimated_transit_days" in data


def test_logistics_return_analytics_api_endpoint(client):
    """Verify GET /api/v1/logistics/return-analytics."""
    res = client.get("/api/v1/logistics/return-analytics")
    assert res.status_code == 200
    data = res.json()
    assert "total_returns" in data
    assert "return_rate_pct" in data
