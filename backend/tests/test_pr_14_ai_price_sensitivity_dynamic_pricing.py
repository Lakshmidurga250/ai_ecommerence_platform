"""
Pytest Test Suite for PR #14: ai-price-sensitivity-dynamic-pricing
Focus: Log-linear price elasticity curve, competitor spread regulator, profit maximizer
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.ai_price_sensitivity_dynamic_pricing import DynamicPricingEngineService, get_dynamic_pricing_engine_service, DynamicPricingEngineServiceRequest
from ai.ai.ai_price_sensitivity_dynamic_pricing_ai_model import DynamicPricingEngineAIModel, get_dynamic_pricing_engine_ai_model
from database.seeds.ai_price_sensitivity_dynamic_pricing_seed import get_seed_data_pr_14, seed_pr_14_to_database

def test_dynamic_pricing_engine_service_initialization():
    """Verify DynamicPricingEngineService singleton instantiation and default attributes."""
    svc = get_dynamic_pricing_engine_service()
    assert svc is not None
    assert svc.domain_name == 'ai-price-sensitivity-dynamic-pricing'
    assert svc.module_version == '3.4.14'

def test_dynamic_pricing_engine_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_dynamic_pricing_engine_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_dynamic_pricing_engine_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_dynamic_pricing_engine_service()
    req = DynamicPricingEngineServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_dynamic_pricing_engine_ai_model_inference():
    """Validate DynamicPricingEngineAIModel probability computation and confidence bounds."""
    model = get_dynamic_pricing_engine_ai_model()
    assert model.MODEL_NAME == 'ai-price-sensitivity-dynamic-pricing-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_dynamic_pricing_engine_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_14()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_14_to_database()
    assert count == len(seeds)
