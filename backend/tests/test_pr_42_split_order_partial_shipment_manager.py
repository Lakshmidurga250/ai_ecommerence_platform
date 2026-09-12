"""
Pytest Test Suite for PR #42: split-order-partial-shipment-manager
Focus: Multi-vendor order splitting, child package tracking IDs, consolidated delivery coordination
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.split_order_partial_shipment_manager import SplitShipmentService, get_split_shipment_service, SplitShipmentServiceRequest
from ai.split.split_order_partial_shipment_manager_ai_model import SplitShipmentAIModel, get_split_shipment_ai_model
from database.seeds.split_order_partial_shipment_manager_seed import get_seed_data_pr_42, seed_pr_42_to_database

def test_split_shipment_service_initialization():
    """Verify SplitShipmentService singleton instantiation and default attributes."""
    svc = get_split_shipment_service()
    assert svc is not None
    assert svc.domain_name == 'split-order-partial-shipment-manager'
    assert svc.module_version == '3.4.42'

def test_split_shipment_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_split_shipment_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res.get('status') != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_split_shipment_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_split_shipment_service()
    req = SplitShipmentServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_split_shipment_ai_model_inference():
    """Validate SplitShipmentAIModel probability computation and confidence bounds."""
    model = get_split_shipment_ai_model()
    assert model.MODEL_NAME == 'split-order-partial-shipment-manager-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_split_shipment_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_42()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_42_to_database()
    assert count == len(seeds)
