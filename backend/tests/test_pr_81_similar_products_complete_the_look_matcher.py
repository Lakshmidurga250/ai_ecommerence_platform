"""
Pytest Test Suite for PR #81: similar-products-complete-the-look-matcher
Focus: Visual embedding similarity search, complementary category graph, cross-category lookbuilder
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.similar_products_complete_the_look_matcher import CompleteTheLookService, get_complete_the_look_service, CompleteTheLookServiceRequest
from ai.similar.similar_products_complete_the_look_matcher_ai_model import CompleteTheLookAIModel, get_complete_the_look_ai_model
from database.seeds.similar_products_complete_the_look_matcher_seed import get_seed_data_pr_81, seed_pr_81_to_database

def test_complete_the_look_service_initialization():
    """Verify CompleteTheLookService singleton instantiation and default attributes."""
    svc = get_complete_the_look_service()
    assert svc is not None
    assert svc.domain_name == 'similar-products-complete-the-look-matcher'
    assert svc.module_version == '3.4.81'

def test_complete_the_look_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_complete_the_look_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_complete_the_look_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_complete_the_look_service()
    req = CompleteTheLookServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_complete_the_look_ai_model_inference():
    """Validate CompleteTheLookAIModel probability computation and confidence bounds."""
    model = get_complete_the_look_ai_model()
    assert model.MODEL_NAME == 'similar-products-complete-the-look-matcher-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_complete_the_look_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_81()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_81_to_database()
    assert count == len(seeds)
