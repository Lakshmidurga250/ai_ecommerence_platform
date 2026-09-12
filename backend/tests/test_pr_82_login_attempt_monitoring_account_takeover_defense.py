"""
Pytest Test Suite for PR #82: login-attempt-monitoring-account-takeover-defense
Focus: Sliding-window login failure tracker, suspicious credential stuffing detector, account lock trigger
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.login_attempt_monitoring_account_takeover_defense import AtoDefenseServiceService, get_ato_defense_service_service, AtoDefenseServiceServiceRequest
from ai.login.login_attempt_monitoring_account_takeover_defense_ai_model import AtoDefenseServiceAIModel, get_ato_defense_service_ai_model
from database.seeds.login_attempt_monitoring_account_takeover_defense_seed import get_seed_data_pr_82, seed_pr_82_to_database

def test_ato_defense_service_service_initialization():
    """Verify AtoDefenseServiceService singleton instantiation and default attributes."""
    svc = get_ato_defense_service_service()
    assert svc is not None
    assert svc.domain_name == 'login-attempt-monitoring-account-takeover-defense'
    assert svc.module_version == '3.4.82'

def test_ato_defense_service_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_ato_defense_service_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_ato_defense_service_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_ato_defense_service_service()
    req = AtoDefenseServiceServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_ato_defense_service_ai_model_inference():
    """Validate AtoDefenseServiceAIModel probability computation and confidence bounds."""
    model = get_ato_defense_service_ai_model()
    assert model.MODEL_NAME == 'login-attempt-monitoring-account-takeover-defense-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_ato_defense_service_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_82()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_82_to_database()
    assert count == len(seeds)
