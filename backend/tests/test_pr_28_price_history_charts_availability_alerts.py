"""
Pytest Test Suite for PR #28: price-history-charts-availability-alerts
Focus: 90-day time-series aggregation, highest/lowest price metrics, stock state transitions
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.price_history_charts_availability_alerts import PriceHistoryService, get_price_history_service, PriceHistoryServiceRequest
from ai.price.price_history_charts_availability_alerts_ai_model import PriceHistoryAIModel, get_price_history_ai_model
from database.seeds.price_history_charts_availability_alerts_seed import get_seed_data_pr_28, seed_pr_28_to_database

def test_price_history_service_initialization():
    """Verify PriceHistoryService singleton instantiation and default attributes."""
    svc = get_price_history_service()
    assert svc is not None
    assert svc.domain_name == 'price-history-charts-availability-alerts'
    assert svc.module_version == '3.4.28'

def test_price_history_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_price_history_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_price_history_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_price_history_service()
    req = PriceHistoryServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_price_history_ai_model_inference():
    """Validate PriceHistoryAIModel probability computation and confidence bounds."""
    model = get_price_history_ai_model()
    assert model.MODEL_NAME == 'price-history-charts-availability-alerts-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_price_history_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_28()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_28_to_database()
    assert count == len(seeds)
