"""
Pytest Test Suite for PR #63: admin-seller-fraud-monitoring-center
Focus: Fraud risk priority queue, manual review action logger (Approve/Reject/Hold), seller freeze triggers
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.admin_seller_fraud_monitoring_center import AdminFraudCenterService, get_admin_fraud_center_service, AdminFraudCenterServiceRequest
from ai.admin.admin_seller_fraud_monitoring_center_ai_model import AdminFraudCenterAIModel, get_admin_fraud_center_ai_model
from database.seeds.admin_seller_fraud_monitoring_center_seed import get_seed_data_pr_63, seed_pr_63_to_database

def test_admin_fraud_center_service_initialization():
    """Verify AdminFraudCenterService singleton instantiation and default attributes."""
    svc = get_admin_fraud_center_service()
    assert svc is not None
    assert svc.domain_name == 'admin-seller-fraud-monitoring-center'
    assert svc.module_version == '3.4.63'

def test_admin_fraud_center_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_admin_fraud_center_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_admin_fraud_center_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_admin_fraud_center_service()
    req = AdminFraudCenterServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_admin_fraud_center_ai_model_inference():
    """Validate AdminFraudCenterAIModel probability computation and confidence bounds."""
    model = get_admin_fraud_center_ai_model()
    assert model.MODEL_NAME == 'admin-seller-fraud-monitoring-center-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_admin_fraud_center_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_63()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_63_to_database()
    assert count == len(seeds)
