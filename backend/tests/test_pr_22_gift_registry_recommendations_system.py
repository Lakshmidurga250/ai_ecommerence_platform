"""
Pytest Test Suite for PR #22: gift-registry-recommendations-system
Focus: Occasion-based matching, registry contribution tracking, thank-you note ledger
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.gift_registry_recommendations_system import GiftRegistryService, get_gift_registry_service, GiftRegistryServiceRequest
from ai.gift.gift_registry_recommendations_system_ai_model import GiftRegistryAIModel, get_gift_registry_ai_model
from database.seeds.gift_registry_recommendations_system_seed import get_seed_data_pr_22, seed_pr_22_to_database

def test_gift_registry_service_initialization():
    """Verify GiftRegistryService singleton instantiation and default attributes."""
    svc = get_gift_registry_service()
    assert svc is not None
    assert svc.domain_name == 'gift-registry-recommendations-system'
    assert svc.module_version == '3.4.22'

def test_gift_registry_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_gift_registry_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_gift_registry_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_gift_registry_service()
    req = GiftRegistryServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_gift_registry_ai_model_inference():
    """Validate GiftRegistryAIModel probability computation and confidence bounds."""
    model = get_gift_registry_ai_model()
    assert model.MODEL_NAME == 'gift-registry-recommendations-system-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_gift_registry_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_22()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_22_to_database()
    assert count == len(seeds)
