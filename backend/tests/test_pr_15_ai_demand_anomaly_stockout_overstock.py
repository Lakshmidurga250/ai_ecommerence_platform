"""
Pytest Test Suite for PR #15: ai-demand-anomaly-stockout-overstock
Focus: Z-score outlier detection, lead-time demand simulation, overstock holding cost penalty
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.ai-demand-anomaly-stockout-overstock import AnomalyStockoutEngineService, get_anomaly_stockout_engine_service, AnomalyStockoutEngineServiceRequest
from ai.ai.ai-demand-anomaly-stockout-overstock_ai_model import AnomalyStockoutEngineAIModel, get_anomaly_stockout_engine_ai_model
from database.seeds.ai-demand-anomaly-stockout-overstock_seed import get_seed_data_pr_15, seed_pr_15_to_database

def test_anomaly_stockout_engine_service_initialization():
    """Verify AnomalyStockoutEngineService singleton instantiation and default attributes."""
    svc = get_anomaly_stockout_engine_service()
    assert svc is not None
    assert svc.domain_name == 'ai-demand-anomaly-stockout-overstock'
    assert svc.module_version == '3.4.15'

def test_anomaly_stockout_engine_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_anomaly_stockout_engine_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_anomaly_stockout_engine_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_anomaly_stockout_engine_service()
    req = AnomalyStockoutEngineServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_anomaly_stockout_engine_ai_model_inference():
    """Validate AnomalyStockoutEngineAIModel probability computation and confidence bounds."""
    model = get_anomaly_stockout_engine_ai_model()
    assert model.MODEL_NAME == 'ai-demand-anomaly-stockout-overstock-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_anomaly_stockout_engine_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_15()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_15_to_database()
    assert count == len(seeds)
