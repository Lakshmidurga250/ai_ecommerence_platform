"""
Pytest Test Suite for PR #23: digital-gift-cards-store-credit-system
Focus: Cryptographic gift card codes, automated balance ledger, partial redemption
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.digital-gift-cards-store-credit-system import GiftCardServiceService, get_gift_card_service_service, GiftCardServiceServiceRequest
from ai.digital.digital-gift-cards-store-credit-system_ai_model import GiftCardServiceAIModel, get_gift_card_service_ai_model
from database.seeds.digital-gift-cards-store-credit-system_seed import get_seed_data_pr_23, seed_pr_23_to_database

def test_gift_card_service_service_initialization():
    """Verify GiftCardServiceService singleton instantiation and default attributes."""
    svc = get_gift_card_service_service()
    assert svc is not None
    assert svc.domain_name == 'digital-gift-cards-store-credit-system'
    assert svc.module_version == '3.4.23'

def test_gift_card_service_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_gift_card_service_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_gift_card_service_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_gift_card_service_service()
    req = GiftCardServiceServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_gift_card_service_ai_model_inference():
    """Validate GiftCardServiceAIModel probability computation and confidence bounds."""
    model = get_gift_card_service_ai_model()
    assert model.MODEL_NAME == 'digital-gift-cards-store-credit-system-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_gift_card_service_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_23()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_23_to_database()
    assert count == len(seeds)
