"""
Tests for Inventory Intelligence (ABC/XYZ Pareto, Warehouse Rebalancing, Multi-Horizon Forecasts)
and AI Dynamic Pricing Engine.
"""

import pytest
from ai.inventory_intelligence.abc_xyz_analyzer import ABCXYZAnalyzer
from ai.pricing.dynamic_pricing_engine import DynamicPricingEngine


@pytest.fixture
def abc_xyz_analyzer(db_session):
    return ABCXYZAnalyzer(db_session)


@pytest.fixture
def pricing_engine(db_session):
    return DynamicPricingEngine(db_session)


def test_abc_xyz_analyzer_init(abc_xyz_analyzer):
    """Verify ABCXYZAnalyzer instantiation."""
    assert abc_xyz_analyzer is not None
    assert hasattr(abc_xyz_analyzer, "generate_matrix")
    assert hasattr(abc_xyz_analyzer, "recommend_transfers")


def test_abc_xyz_matrix_generation(abc_xyz_analyzer):
    """Verify ABC/XYZ 9-box matrix classification."""
    matrix = abc_xyz_analyzer.generate_matrix()
    assert isinstance(matrix, list)
    assert len(matrix) > 0

    first = matrix[0]
    assert "product_id" in first
    assert "abc_class" in first
    assert "xyz_class" in first
    assert first["abc_class"] in ["A", "B", "C"]
    assert first["xyz_class"] in ["X", "Y", "Z"]
    assert "matrix_tag" in first
    assert "stockout_risk_score" in first


def test_warehouse_transfer_recommendations(abc_xyz_analyzer):
    """Verify automated transfer recommendations between regional warehouses."""
    transfers = abc_xyz_analyzer.recommend_transfers()
    assert isinstance(transfers, list)
    for t in transfers:
        assert "transfer_id" in t
        assert "product_id" in t
        assert "source_warehouse_id" in t
        assert "target_warehouse_id" in t
        assert t["transfer_quantity"] > 0


def test_inventory_matrix_api_endpoint(client):
    """Verify GET /api/v1/inventory-intelligence/matrix."""
    res = client.get("/api/v1/inventory-intelligence/matrix")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_inventory_transfers_api_endpoint(client):
    """Verify GET /api/v1/inventory-intelligence/transfers."""
    res = client.get("/api/v1/inventory-intelligence/transfers")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_multi_horizon_forecast_api_endpoint(client):
    """Verify GET /api/v1/inventory-intelligence/multi-horizon-forecast/{product_id}."""
    res = client.get("/api/v1/inventory-intelligence/multi-horizon-forecast/1")
    assert res.status_code == 200
    data = res.json()
    assert "product_id" in data
    assert "horizons" in data
    assert "day_7" in data["horizons"]
    assert "day_14" in data["horizons"]
    assert "day_30" in data["horizons"]


def test_dynamic_pricing_engine_init(pricing_engine):
    """Verify DynamicPricingEngine instantiation."""
    assert pricing_engine is not None
    assert hasattr(pricing_engine, "generate_recommendations")


def test_dynamic_pricing_recommendations_structure(pricing_engine):
    """Verify pricing recommendations have elasticity and revenue shift."""
    recs = pricing_engine.generate_recommendations(limit=5)
    assert isinstance(recs, list)
    assert len(recs) > 0

    first = recs[0]
    assert "product_id" in first
    assert "current_price" in first
    assert "recommended_price" in first
    assert "elasticity" in first
    assert "strategy" in first
    assert "expected_demand_lift_pct" in first
    assert "expected_revenue_shift_pct" in first
    assert "rationale" in first


def test_dynamic_pricing_strategy_filter(pricing_engine):
    """Verify strategy filtering works in pricing engine."""
    recs = pricing_engine.generate_recommendations(strategy="MARGIN_MAXIMIZATION")
    assert isinstance(recs, list)
    for r in recs:
        assert r["strategy"] == "MARGIN_MAXIMIZATION"


def test_seller_pricing_recommendations_endpoint(client, seller_token):
    """Verify GET /api/v1/marketplace/pricing-recommendations with seller auth."""
    res = client.get(
        "/api/v1/marketplace/pricing-recommendations",
        headers={"Authorization": f"Bearer {seller_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_product_pricing_recommendation_endpoint(client):
    """Verify GET /api/v1/marketplace/pricing-recommendations/product/{product_id}."""
    res = client.get("/api/v1/marketplace/pricing-recommendations/product/1")
    assert res.status_code == 200
    data = res.json()
    assert data["product_id"] == 1
    assert "recommended_price" in data


def test_seller_pricing_unauthorized(client):
    """Verify unauthenticated access to seller pricing recommendations."""
    res = client.get("/api/v1/marketplace/pricing-recommendations")
    # Public or seller endpoint
    assert res.status_code in [200, 401]
