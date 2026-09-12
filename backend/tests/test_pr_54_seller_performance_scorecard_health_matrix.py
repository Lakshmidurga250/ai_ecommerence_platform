"""
Pytest Test Suite for PR #54: seller-performance-scorecard-health-matrix
Focus: Late dispatch rate metric, order cancellation rate, customer dispute score, tier badge rating
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.seller_performance_scorecard_health_matrix import SellerHealthService, get_seller_health_service, SellerHealthServiceRequest
from ai.seller.seller_performance_scorecard_health_matrix_ai_model import SellerHealthAIModel, get_seller_health_ai_model
from database.seeds.seller_performance_scorecard_health_matrix_seed import get_seed_data_pr_54, seed_pr_54_to_database

def test_seller_health_service_initialization():
    """Verify SellerHealthService singleton instantiation and default attributes."""
    svc = get_seller_health_service()
    assert svc is not None
    assert svc.domain_name == 'seller-performance-scorecard-health-matrix'
    assert svc.module_version == '3.4.54'

def test_seller_health_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_seller_health_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_seller_health_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_seller_health_service()
    req = SellerHealthServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_seller_health_ai_model_inference():
    """Validate SellerHealthAIModel probability computation and confidence bounds."""
    model = get_seller_health_ai_model()
    assert model.MODEL_NAME == 'seller-performance-scorecard-health-matrix-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_seller_health_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_54()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_54_to_database()
    assert count == len(seeds)
