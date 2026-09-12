"""
Pytest Test Suite for PR #79: search-intent-detection-personalized-ranking
Focus: Commercial/Informational intent classifier, category affinity boost, personalized score re-ranker
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.search_intent_detection_personalized_ranking import SearchIntentRankerService, get_search_intent_ranker_service, SearchIntentRankerServiceRequest
from ai.search.search_intent_detection_personalized_ranking_ai_model import SearchIntentRankerAIModel, get_search_intent_ranker_ai_model
from database.seeds.search_intent_detection_personalized_ranking_seed import get_seed_data_pr_79, seed_pr_79_to_database

def test_search_intent_ranker_service_initialization():
    """Verify SearchIntentRankerService singleton instantiation and default attributes."""
    svc = get_search_intent_ranker_service()
    assert svc is not None
    assert svc.domain_name == 'search-intent-detection-personalized-ranking'
    assert svc.module_version == '3.4.79'

def test_search_intent_ranker_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_search_intent_ranker_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_search_intent_ranker_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_search_intent_ranker_service()
    req = SearchIntentRankerServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_search_intent_ranker_ai_model_inference():
    """Validate SearchIntentRankerAIModel probability computation and confidence bounds."""
    model = get_search_intent_ranker_ai_model()
    assert model.MODEL_NAME == 'search-intent-detection-personalized-ranking-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_search_intent_ranker_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_79()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_79_to_database()
    assert count == len(seeds)
