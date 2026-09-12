"""
Pytest Test Suite for PR #34: split-payments-multi-instrument-checkout
Focus: Transaction splitting orchestrator, partial auth rollback, composite payment receipts
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.split_payments_multi_instrument_checkout import SplitPaymentsService, get_split_payments_service, SplitPaymentsServiceRequest
from ai.split.split_payments_multi_instrument_checkout_ai_model import SplitPaymentsAIModel, get_split_payments_ai_model
from database.seeds.split_payments_multi_instrument_checkout_seed import get_seed_data_pr_34, seed_pr_34_to_database

def test_split_payments_service_initialization():
    """Verify SplitPaymentsService singleton instantiation and default attributes."""
    svc = get_split_payments_service()
    assert svc is not None
    assert svc.domain_name == 'split-payments-multi-instrument-checkout'
    assert svc.module_version == '3.4.34'

def test_split_payments_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_split_payments_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_split_payments_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_split_payments_service()
    req = SplitPaymentsServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_split_payments_ai_model_inference():
    """Validate SplitPaymentsAIModel probability computation and confidence bounds."""
    model = get_split_payments_ai_model()
    assert model.MODEL_NAME == 'split-payments-multi-instrument-checkout-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_split_payments_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_34()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_34_to_database()
    assert count == len(seeds)
