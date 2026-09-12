"""
Test Suite: Next-Best-Action (NBA) & Personalized Ranking Model.
Tests contextual commercial decision heuristics (cart recovery, review solicitation, loyalty tiers)
and multi-factor personalized re-ranking algorithms.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from ai.customer_intelligence.next_best_action import NextBestActionEngine
from ai.recommendations.personalized_ranker import PersonalizedRanker

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_next_best_action_prediction(db_session):
    engine = NextBestActionEngine(db_session)
    user = db_session.query(User).first()
    assert user is not None

    action = engine.predict_next_best_action(user_id=user.id)
    assert "error" not in action
    assert action["user_id"] == user.id
    assert "action_type" in action
    assert "headline" in action
    assert "cta_label" in action
    assert "confidence" in action
    assert action["confidence"] > 0.5


def test_next_best_action_invalid_user(db_session):
    engine = NextBestActionEngine(db_session)
    res = engine.predict_next_best_action(user_id=999999)
    assert "error" in res


def test_personalized_ranking_cold_start(db_session):
    ranker = PersonalizedRanker(db_session)
    products = db_session.query(Product).filter(Product.is_active == True).limit(10).all()

    # Anonymous / cold start user
    ranked = ranker.rank_products_for_user(products=products, user_id=None, limit=5)
    assert len(ranked) == 5
    assert ranked[0]["rank"] == 1
    assert "personalized_score" in ranked[0]
    assert len(ranked[0]["ranking_reasons"]) > 0


def test_personalized_ranking_with_user_history(db_session):
    ranker = PersonalizedRanker(db_session)
    user = db_session.query(User).first()
    products = db_session.query(Product).filter(Product.is_active == True).limit(15).all()

    ranked = ranker.rank_products_for_user(products=products, user_id=user.id, limit=8)
    assert len(ranked) == 8
    # Ensure ranked in descending order of score
    scores = [r["personalized_score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)


def test_api_next_best_action_endpoint():
    res = client.get("/api/v1/commerce/next-best-action/1")
    assert res.status_code == 200
    data = res.json()
    assert "action_type" in data
    assert "headline" in data
    assert "target_route" in data


def test_api_personalized_ranking_endpoint():
    res = client.post(
        "/api/v1/recommendations-v3/personalized-ranking",
        json={"user_id": 1, "limit": 6}
    )
    assert res.status_code == 200
    data = res.json()
    assert "ranked_results" in data
    assert len(data["ranked_results"]) <= 6
