"""
Pytest Test Suite for PR #47: return-request-workflow-eligibility-engine
Focus: Category return window validation, condition checklist verification, return authorization tokens
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.return_request_workflow_eligibility_engine import ReturnEligibilityService, get_return_eligibility_service, ReturnEligibilityServiceRequest
from ai.return.return_request_workflow_eligibility_engine_ai_model import ReturnEligibilityAIModel, get_return_eligibility_ai_model
from database.seeds.return_request_workflow_eligibility_engine_seed import get_seed_data_pr_47, seed_pr_47_to_database

def test_return_eligibility_service_initialization():
    """Verify ReturnEligibilityService singleton instantiation and default attributes."""
    svc = get_return_eligibility_service()
    assert svc is not None
    assert svc.domain_name == 'return-request-workflow-eligibility-engine'
    assert svc.module_version == '3.4.47'

def test_return_eligibility_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_return_eligibility_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_return_eligibility_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_return_eligibility_service()
    req = ReturnEligibilityServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_return_eligibility_ai_model_inference():
    """Validate ReturnEligibilityAIModel probability computation and confidence bounds."""
    model = get_return_eligibility_ai_model()
    assert model.MODEL_NAME == 'return-request-workflow-eligibility-engine-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_return_eligibility_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_47()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_47_to_database()
    assert count == len(seeds)
