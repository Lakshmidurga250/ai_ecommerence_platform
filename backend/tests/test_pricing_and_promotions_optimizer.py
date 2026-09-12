"""
Test Suite: Promotion Optimization & Price Elasticity Simulation.
Tests demand response curves, discrete promotional discount tiers, breakeven sales lifts,
and profit-maximizing recommendation objectives.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.product import Product
from ai.pricing.promotion_optimizer import PromotionOptimizer

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_promotion_optimizer_profit_maximization(db_session):
    optimizer = PromotionOptimizer(db_session)
    prod = db_session.query(Product).first()
    assert prod is not None

    res = optimizer.optimize_promotion(
        product_id=prod.id,
        target_objective="MAX_PROFIT",
        baseline_weekly_sales=30
    )
    assert "error" not in res
    assert res["product_id"] == prod.id
    assert res["target_objective"] == "MAX_PROFIT"
    assert "recommended_promotion" in res
    assert res["recommended_promotion"]["optimal_discount_pct"] >= 0.0
    assert len(res["all_tier_simulations"]) == len(PromotionOptimizer.DEFAULT_DISCOUNT_TIERS)


def test_promotion_optimizer_revenue_maximization(db_session):
    optimizer = PromotionOptimizer(db_session)
    prod = db_session.query(Product).first()

    res = optimizer.optimize_promotion(
        product_id=prod.id,
        target_objective="MAX_REVENUE",
        baseline_weekly_sales=20
    )
    assert "error" not in res
    assert res["target_objective"] == "MAX_REVENUE"
    assert "expected_weekly_revenue" in res["recommended_promotion"]


def test_promotion_optimizer_all_tiers_calculated(db_session):
    optimizer = PromotionOptimizer(db_session)
    prod = db_session.query(Product).first()

    res = optimizer.optimize_promotion(product_id=prod.id)
    sims = res["all_tier_simulations"]
    discounts = [s["discount_pct"] for s in sims]
    assert 0.0 in discounts
    assert 10.0 in discounts
    assert 20.0 in discounts

    # Verify that volume lift increases with discount percentage
    assert sims[-1]["volume_lift_pct"] > sims[0]["volume_lift_pct"]


def test_promotion_optimizer_product_not_found(db_session):
    optimizer = PromotionOptimizer(db_session)
    res = optimizer.optimize_promotion(product_id=999999)
    assert "error" in res


def test_api_promotion_optimizer_endpoint():
    prod_res = client.get("/api/v1/products?limit=1")
    res_data = prod_res.json()
    products = res_data if isinstance(res_data, list) else res_data.get("products", [])
    prod_id = products[0]["id"]

    res = client.post(
        "/api/v1/commerce/promotion-optimize",
        json={"product_id": prod_id, "target_objective": "MAX_PROFIT", "baseline_weekly_sales": 25}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["product_id"] == prod_id
    assert "recommended_promotion" in data
    assert "all_tier_simulations" in data


def test_api_promotion_optimizer_not_found():
    res = client.post(
        "/api/v1/commerce/promotion-optimize",
        json={"product_id": 999999}
    )
    assert res.status_code == 404
