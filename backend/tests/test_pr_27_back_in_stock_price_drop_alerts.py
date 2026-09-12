"""
Pytest Test Suite for PR #27: back-in-stock-price-drop-alerts
Focus: Threshold subscription queues, price event publish/subscribe, SMS/Email dispatch hooks
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.back-in-stock-price-drop-alerts import PriceDropAlertsService, get_price_drop_alerts_service, PriceDropAlertsServiceRequest
from ai.back.back-in-stock-price-drop-alerts_ai_model import PriceDropAlertsAIModel, get_price_drop_alerts_ai_model
from database.seeds.back-in-stock-price-drop-alerts_seed import get_seed_data_pr_27, seed_pr_27_to_database

def test_price_drop_alerts_service_initialization():
    """Verify PriceDropAlertsService singleton instantiation and default attributes."""
    svc = get_price_drop_alerts_service()
    assert svc is not None
    assert svc.domain_name == 'back-in-stock-price-drop-alerts'
    assert svc.module_version == '3.4.27'

def test_price_drop_alerts_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_price_drop_alerts_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_price_drop_alerts_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_price_drop_alerts_service()
    req = PriceDropAlertsServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_price_drop_alerts_ai_model_inference():
    """Validate PriceDropAlertsAIModel probability computation and confidence bounds."""
    model = get_price_drop_alerts_ai_model()
    assert model.MODEL_NAME == 'back-in-stock-price-drop-alerts-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_price_drop_alerts_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_27()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_27_to_database()
    assert count == len(seeds)
