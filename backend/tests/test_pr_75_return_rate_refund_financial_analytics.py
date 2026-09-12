"""
Pytest Test Suite for PR #75: return-rate-refund-financial-analytics
Focus: Return rate by vendor/category, refund loss ledger, restocking fee optimization model
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.return-rate-refund-financial-analytics import ReturnsFinancialBiService, get_returns_financial_bi_service, ReturnsFinancialBiServiceRequest
from ai.return.return-rate-refund-financial-analytics_ai_model import ReturnsFinancialBiAIModel, get_returns_financial_bi_ai_model
from database.seeds.return-rate-refund-financial-analytics_seed import get_seed_data_pr_75, seed_pr_75_to_database

def test_returns_financial_bi_service_initialization():
    """Verify ReturnsFinancialBiService singleton instantiation and default attributes."""
    svc = get_returns_financial_bi_service()
    assert svc is not None
    assert svc.domain_name == 'return-rate-refund-financial-analytics'
    assert svc.module_version == '3.4.75'

def test_returns_financial_bi_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_returns_financial_bi_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_returns_financial_bi_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_returns_financial_bi_service()
    req = ReturnsFinancialBiServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_returns_financial_bi_ai_model_inference():
    """Validate ReturnsFinancialBiAIModel probability computation and confidence bounds."""
    model = get_returns_financial_bi_ai_model()
    assert model.MODEL_NAME == 'return-rate-refund-financial-analytics-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_returns_financial_bi_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_75()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_75_to_database()
    assert count == len(seeds)
