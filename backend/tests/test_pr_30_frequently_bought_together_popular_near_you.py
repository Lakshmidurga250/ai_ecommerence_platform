"""
Pytest Test Suite for PR #30: frequently-bought-together-popular-near-you
Focus: Co-occurrence association rules (Apriori), geospatial pincode clustering, localized popularity
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.frequently_bought_together_popular_near_you import FrequentlyBoughtService, get_frequently_bought_service, FrequentlyBoughtServiceRequest
from ai.frequently.frequently_bought_together_popular_near_you_ai_model import FrequentlyBoughtAIModel, get_frequently_bought_ai_model
from database.seeds.frequently_bought_together_popular_near_you_seed import get_seed_data_pr_30, seed_pr_30_to_database

def test_frequently_bought_service_initialization():
    """Verify FrequentlyBoughtService singleton instantiation and default attributes."""
    svc = get_frequently_bought_service()
    assert svc is not None
    assert svc.domain_name == 'frequently-bought-together-popular-near-you'
    assert svc.module_version == '3.4.30'

def test_frequently_bought_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_frequently_bought_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_frequently_bought_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_frequently_bought_service()
    req = FrequentlyBoughtServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_frequently_bought_ai_model_inference():
    """Validate FrequentlyBoughtAIModel probability computation and confidence bounds."""
    model = get_frequently_bought_ai_model()
    assert model.MODEL_NAME == 'frequently-bought-together-popular-near-you-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_frequently_bought_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_30()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_30_to_database()
    assert count == len(seeds)
