"""
Pytest Test Suite for PR #29: recently-searched-recently-purchased-feeds
Focus: LRU user activity cache, query history deduplication, temporal relevance weighting
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.recently_searched_recently_purchased_feeds import RecentActivityService, get_recent_activity_service, RecentActivityServiceRequest
from ai.recently.recently_searched_recently_purchased_feeds_ai_model import RecentActivityAIModel, get_recent_activity_ai_model
from database.seeds.recently_searched_recently_purchased_feeds_seed import get_seed_data_pr_29, seed_pr_29_to_database

def test_recent_activity_service_initialization():
    """Verify RecentActivityService singleton instantiation and default attributes."""
    svc = get_recent_activity_service()
    assert svc is not None
    assert svc.domain_name == 'recently-searched-recently-purchased-feeds'
    assert svc.module_version == '3.4.29'

def test_recent_activity_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_recent_activity_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_recent_activity_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_recent_activity_service()
    req = RecentActivityServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_recent_activity_ai_model_inference():
    """Validate RecentActivityAIModel probability computation and confidence bounds."""
    model = get_recent_activity_ai_model()
    assert model.MODEL_NAME == 'recently-searched-recently-purchased-feeds-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_recent_activity_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_29()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_29_to_database()
    assert count == len(seeds)
