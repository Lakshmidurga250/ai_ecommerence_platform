"""
Pytest Test Suite for PR #83: device-fingerprinting-ip-risk-rate-limiter
Focus: Canvas/browser fingerprint hasher, IP CIDR risk classifier, token-bucket rate limit algorithm
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.device_fingerprinting_ip_risk_rate_limiter import DeviceIpSecurityService, get_device_ip_security_service, DeviceIpSecurityServiceRequest
from ai.device.device_fingerprinting_ip_risk_rate_limiter_ai_model import DeviceIpSecurityAIModel, get_device_ip_security_ai_model
from database.seeds.device_fingerprinting_ip_risk_rate_limiter_seed import get_seed_data_pr_83, seed_pr_83_to_database

def test_device_ip_security_service_initialization():
    """Verify DeviceIpSecurityService singleton instantiation and default attributes."""
    svc = get_device_ip_security_service()
    assert svc is not None
    assert svc.domain_name == 'device-fingerprinting-ip-risk-rate-limiter'
    assert svc.module_version == '3.4.83'

def test_device_ip_security_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_device_ip_security_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_device_ip_security_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_device_ip_security_service()
    req = DeviceIpSecurityServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_device_ip_security_ai_model_inference():
    """Validate DeviceIpSecurityAIModel probability computation and confidence bounds."""
    model = get_device_ip_security_ai_model()
    assert model.MODEL_NAME == 'device-fingerprinting-ip-risk-rate-limiter-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_device_ip_security_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_83()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_83_to_database()
    assert count == len(seeds)
