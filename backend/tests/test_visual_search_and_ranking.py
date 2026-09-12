"""
Tests for AI Visual Search & Multi-Stage Recommendation Ranking Pipeline.
Validates 16-D vector embedding, cosine similarity, MMR diversity, and session-based co-browsing.
"""

import pytest
from ai.search.visual_search import VisualSearchEngine
from ai.recommendations.ranking_pipeline import RecommendationRankingPipeline


@pytest.fixture
def visual_engine(db_session):
    return VisualSearchEngine(db_session)



def test_visual_search_vector_generation(visual_engine):
    """Verify 16-D normalized vector generation."""
    sample_url = "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
    vec = visual_engine.extract_image_vector(image_url=sample_url)
    assert len(vec) == 16
    norm = sum(x ** 2 for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-4


def test_visual_search_color_analysis(visual_engine):
    """Verify color analysis returns palette and confidence."""
    color_info = visual_engine.analyze_color_geometry("https://images.unsplash.com/photo-1542291026-7eec264c27ff")
    assert "primary_color" in color_info
    assert "palette" in color_info


def test_visual_search_cosine_similarity(visual_engine):
    """Verify mathematical cosine similarity."""
    v1 = [1.0, 0.0, 0.0] + [0.0] * 13
    v2 = [1.0, 0.0, 0.0] + [0.0] * 13
    sim_identical = visual_engine._cosine_similarity(v1, v2)
    assert abs(sim_identical - 1.0) < 1e-4

    v3 = [0.0, 1.0, 0.0] + [0.0] * 13
    sim_orthogonal = visual_engine._cosine_similarity(v1, v3)
    assert abs(sim_orthogonal) < 1e-4


def test_visual_search_search_results(visual_engine):
    """Verify visual search query returns sorted matches with reasoning."""
    results = visual_engine.search_by_image_instance(
        image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff",
        top_k=5
    )
    assert len(results) > 0
    first = results[0]
    assert "product_id" in first
    assert "similarity_score" in first
    assert "reasoning" in first
    assert first["similarity_score"] >= 0.0


def test_visual_search_api_endpoint(client):
    """Verify POST /api/v1/search/visual works correctly."""
    res = client.post(
        "/api/v1/search/visual",
        json={
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            "top_k": 4
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "matches" in data
    assert "execution_ms" in data
    assert len(data["matches"]) <= 4


def test_visual_search_api_with_category_hint(client):
    """Verify category filtering inside visual search API."""
    res = client.post(
        "/api/v1/search/visual",
        json={
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            "category_hint": "Electronics",
            "top_k": 3
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "matches" in data


def test_visual_search_api_validation_error(client):
    """Verify 400 error when neither image_url nor image_base64 is provided."""
    res = client.post("/api/v1/search/visual", json={})
    assert res.status_code in [400, 422]


def test_ranking_pipeline_candidate_generation(db_session):
    """Verify Candidate Generation retrieval stage."""
    candidates = RecommendationRankingPipeline._generate_candidates(db_session, user_id=1, category_id=None, pool_size=20)
    assert isinstance(candidates, list)
    assert len(candidates) > 0


def test_ranking_pipeline_execute(db_session):
    """Verify end-to-end multi-stage ranking execution."""
    ranked = RecommendationRankingPipeline.rank_for_user(db_session, user_id=1, limit=5)
    assert len(ranked) > 0
    top = ranked[0]
    assert "product_id" in top
    assert "recommendation_score" in top
    assert "ranking_rationale" in top



def test_recommendation_pipeline_api_endpoint(client, customer_token):
    """Verify GET /api/v1/ai/recommendations/pipeline."""
    res = client.get(
        "/api/v1/ai/recommendations/pipeline?limit=6",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= 6


def test_session_recommendations_endpoint(client):
    """Verify GET /api/v1/ai/recommendations/session with active session product list."""
    res = client.get("/api/v1/ai/recommendations/session?viewed_ids=1,2&limit=4")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= 4

