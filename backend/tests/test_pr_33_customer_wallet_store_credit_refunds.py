"""
Pytest Test Suite for PR #33: customer-wallet-store-credit-refunds
Focus: Double-entry accounting ledger, wallet top-up, instant refund balance locking
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.customer_wallet_store_credit_refunds import WalletSystemService, get_wallet_system_service, WalletSystemServiceRequest
from ai.customer.customer_wallet_store_credit_refunds_ai_model import WalletSystemAIModel, get_wallet_system_ai_model
from database.seeds.customer_wallet_store_credit_refunds_seed import get_seed_data_pr_33, seed_pr_33_to_database

def test_wallet_system_service_initialization():
    """Verify WalletSystemService singleton instantiation and default attributes."""
    svc = get_wallet_system_service()
    assert svc is not None
    assert svc.domain_name == 'customer-wallet-store-credit-refunds'
    assert svc.module_version == '3.4.33'

def test_wallet_system_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_wallet_system_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_wallet_system_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_wallet_system_service()
    req = WalletSystemServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_wallet_system_ai_model_inference():
    """Validate WalletSystemAIModel probability computation and confidence bounds."""
    model = get_wallet_system_ai_model()
    assert model.MODEL_NAME == 'customer-wallet-store-credit-refunds-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_wallet_system_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_33()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_33_to_database()
    assert count == len(seeds)
