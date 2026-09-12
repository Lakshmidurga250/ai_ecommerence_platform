"""
Test Suite: Returns Intelligence, Review Quality & Product Quality Scoring.
Tests category return volatility, return policy evaluation, spam review heuristics,
and Bayesian product quality indices.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.product import Product
from ai.returns.return_predictor import ReturnPredictor
from ai.sentiment.review_quality_detector import ReviewQualityDetector
from ai.sentiment.product_quality_scorer import ProductQualityScorer
from backend.app.services.returns_intelligence_service import ReturnsIntelligenceService

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_return_predictor_footwear_high_risk(db_session):
    predictor = ReturnPredictor(db_session)
    prod = db_session.query(Product).join(Product.category).filter(Product.category.has(slug="footwear-running")).first()
    if not prod:
        prod = db_session.query(Product).first()

    res = predictor.predict_return_risk(product_id=prod.id)
    assert "error" not in res
    assert res["product_id"] == prod.id
    assert 0.0 < res["predicted_return_probability"] <= 1.0
    assert len(res["identified_risk_factors"]) > 0
    assert len(res["preventative_mitigations"]) > 0


def test_return_predictor_stationery_low_risk(db_session):
    predictor = ReturnPredictor(db_session)
    prod = db_session.query(Product).join(Product.category).filter(Product.category.has(slug="books-stationery")).first()
    if prod:
        res = predictor.predict_return_risk(product_id=prod.id)
        assert res["risk_level"] == "LOW"


def test_review_quality_detector_high_quality():
    detector = ReviewQualityDetector()
    detailed_text = "The audio frequency response on these headphones is exceptional. Bass is punchy without distorting highs, and the battery easily lasted 28 hours during international transit. Highly recommended for audiophiles."
    res = detector.evaluate_review_quality(comment=detailed_text, rating=5, is_verified_purchase=True)
    assert res["quality_score"] >= 75.0
    assert res["quality_tier"] == "HIGH_QUALITY_DETAILED"
    assert res["is_spam"] == False
    assert res["is_helpful"] == True


def test_review_quality_detector_spam():
    detector = ReviewQualityDetector()
    spam_text = "FREE MONEY visit https://spam-free-cash.xyz and call me on whatsapp right now!!!!!!!"
    res = detector.evaluate_review_quality(comment=spam_text, rating=5, is_verified_purchase=False)
    assert res["is_spam"] == True
    assert res["quality_score"] <= 20.0
    assert res["quality_tier"] == "SUSPICIOUS_SPAM"


def test_review_quality_detector_rating_discrepancy():
    detector = ReviewQualityDetector()
    discrepant = "Worst terrible product ever broke completely on day one garbage"
    res = detector.evaluate_review_quality(comment=discrepant, rating=5, is_verified_purchase=True)
    assert "Rating-sentiment contradiction" in res["flags"][0]


def test_product_quality_scorer(db_session):
    scorer = ProductQualityScorer(db_session)
    prod = db_session.query(Product).first()
    assert prod is not None

    res = scorer.calculate_quality_score(product_id=prod.id)
    assert "error" not in res
    assert 0.0 <= res["composite_quality_score"] <= 100.0
    assert "quality_badge" in res
    assert "breakdown" in res
    assert "bayesian_rating_score" in res["breakdown"]


def test_api_returns_dashboard_endpoint():
    res = client.get("/api/v1/commerce/returns-dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "returns_kpis" in data
    assert "top_return_reasons" in data
    assert "category_return_rates" in data


def test_api_product_quality_endpoint():
    res = client.get("/api/v1/commerce/product-quality/1")
    assert res.status_code == 200
    data = res.json()
    assert "composite_quality_score" in data
    assert "quality_badge" in data


def test_api_review_quality_check_endpoint():
    res = client.post(
        "/api/v1/commerce/review-quality-check",
        json={"comment": "Excellent build quality and great sound output.", "rating": 5, "is_verified_purchase": True}
    )
    assert res.status_code == 200
    data = res.json()
    assert "quality_score" in data
    assert data["is_spam"] == False
