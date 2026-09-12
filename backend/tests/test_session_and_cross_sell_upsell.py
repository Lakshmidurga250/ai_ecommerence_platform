"""
Test Suite: Session-Based Recommendations, Cross-Sell & Upsell Prediction.
Tests Markov transition clickstream prediction, frequently bought together association lift,
and trade-up alternative discovery.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.product import Product
from ai.recommendations.session_recommender import SessionRecommender
from ai.recommendations.cross_sell_upsell import CrossSellUpsellPredictor

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_session_recommender_with_history(db_session):
    recommender = SessionRecommender(db_session)
    products = db_session.query(Product).filter(Product.is_active == True).limit(3).all()
    session_ids = [p.id for p in products]

    res = recommender.recommend_for_session(session_product_ids=session_ids, limit=4)
    assert "error" not in res
    assert res["session_items_analyzed"] == len(session_ids)
    assert res["strategy"] == "MARKOV_SESSION_TRANSITION"
    assert len(res["recommendations"]) <= 4
    # Ensure viewed items are not recommended
    rec_ids = [r["id"] for r in res["recommendations"]]
    for sid in session_ids:
        assert sid not in rec_ids


def test_session_recommender_empty_session(db_session):
    recommender = SessionRecommender(db_session)
    res = recommender.recommend_for_session(session_product_ids=[], limit=5)
    assert "error" not in res
    assert res["strategy"] == "FALLBACK_POPULAR"
    assert len(res["recommendations"]) == 5


def test_cross_sell_prediction(db_session):
    predictor = CrossSellUpsellPredictor(db_session)
    prod = db_session.query(Product).filter(Product.price > 10000).first()
    assert prod is not None

    res = predictor.predict_cross_sell(product_id=prod.id, limit=3)
    assert "error" not in res
    assert "focal_product" in res
    assert "cross_sell_items" in res
    assert len(res["cross_sell_items"]) <= 3

    for item in res["cross_sell_items"]:
        assert item["price"] <= prod.price
        assert item["co_occurrence_lift"] >= 1.0
        assert item["combo_price_with_focal"] > 0


def test_upsell_prediction(db_session):
    predictor = CrossSellUpsellPredictor(db_session)
    # Find a product with moderate price
    prod = db_session.query(Product).filter(Product.price >= 2000, Product.price <= 30000).first()
    if not prod:
        prod = db_session.query(Product).first()

    res = predictor.predict_upsell(product_id=prod.id, limit=3)
    assert "error" not in res
    assert "upsell_alternatives" in res
    for item in res["upsell_alternatives"]:
        assert item["price"] >= prod.price
        assert len(item["key_advantages"]) > 0


def test_api_session_recommendations_endpoint():
    res = client.post(
        "/api/v1/recommendations-v3/session-recommendations",
        json={"session_product_ids": [1, 2], "limit": 4}
    )
    assert res.status_code == 200
    data = res.json()
    assert "recommendations" in data


def test_api_cross_sell_endpoint():
    res = client.get("/api/v1/recommendations-v3/cross-sell/1?limit=2")
    assert res.status_code == 200
    data = res.json()
    assert "cross_sell_items" in data


def test_api_upsell_endpoint():
    res = client.get("/api/v1/recommendations-v3/upsell/1?limit=2")
    assert res.status_code == 200
    data = res.json()
    assert "upsell_alternatives" in data
