"""
Pytest Test Suite for PR #40: shipment-tracking-timeline-milestone-fsm
Focus: Carrier milestone event parser, live progress percentage estimator, milestone status history
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.shipment_tracking_timeline_milestone_fsm import ShipmentFsmService, get_shipment_fsm_service, ShipmentFsmServiceRequest
from ai.shipment.shipment_tracking_timeline_milestone_fsm_ai_model import ShipmentFsmAIModel, get_shipment_fsm_ai_model
from database.seeds.shipment_tracking_timeline_milestone_fsm_seed import get_seed_data_pr_40, seed_pr_40_to_database

def test_shipment_fsm_service_initialization():
    """Verify ShipmentFsmService singleton instantiation and default attributes."""
    svc = get_shipment_fsm_service()
    assert svc is not None
    assert svc.domain_name == 'shipment-tracking-timeline-milestone-fsm'
    assert svc.module_version == '3.4.40'

def test_shipment_fsm_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_shipment_fsm_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_shipment_fsm_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_shipment_fsm_service()
    req = ShipmentFsmServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_shipment_fsm_ai_model_inference():
    """Validate ShipmentFsmAIModel probability computation and confidence bounds."""
    model = get_shipment_fsm_ai_model()
    assert model.MODEL_NAME == 'shipment-tracking-timeline-milestone-fsm-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_shipment_fsm_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_40()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_40_to_database()
    assert count == len(seeds)
