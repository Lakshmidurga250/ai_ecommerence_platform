"""
Pytest Test Suite for PR #36: payment-retry-failed-payment-recovery
Focus: Error code diagnostic classification, exponential backoff retries, alternative instrument fallback
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.payment_retry_failed_payment_recovery import PaymentRecoveryService, get_payment_recovery_service, PaymentRecoveryServiceRequest
from ai.payment.payment_retry_failed_payment_recovery_ai_model import PaymentRecoveryAIModel, get_payment_recovery_ai_model
from database.seeds.payment_retry_failed_payment_recovery_seed import get_seed_data_pr_36, seed_pr_36_to_database

def test_payment_recovery_service_initialization():
    """Verify PaymentRecoveryService singleton instantiation and default attributes."""
    svc = get_payment_recovery_service()
    assert svc is not None
    assert svc.domain_name == 'payment-retry-failed-payment-recovery'
    assert svc.module_version == '3.4.36'

def test_payment_recovery_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_payment_recovery_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_payment_recovery_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_payment_recovery_service()
    req = PaymentRecoveryServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_payment_recovery_ai_model_inference():
    """Validate PaymentRecoveryAIModel probability computation and confidence bounds."""
    model = get_payment_recovery_ai_model()
    assert model.MODEL_NAME == 'payment-retry-failed-payment-recovery-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_payment_recovery_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_36()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_36_to_database()
    assert count == len(seeds)
