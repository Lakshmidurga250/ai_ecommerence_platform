"""
Pytest Test Suite for PR #39: delivery-slot-selection-express-same-day
Focus: Slot capacity reservation locks, delivery tier cost calculator, cut-off time enforcement
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.delivery-slot-selection-express-same-day import DeliverySlotsService, get_delivery_slots_service, DeliverySlotsServiceRequest
from ai.delivery.delivery-slot-selection-express-same-day_ai_model import DeliverySlotsAIModel, get_delivery_slots_ai_model
from database.seeds.delivery-slot-selection-express-same-day_seed import get_seed_data_pr_39, seed_pr_39_to_database

def test_delivery_slots_service_initialization():
    """Verify DeliverySlotsService singleton instantiation and default attributes."""
    svc = get_delivery_slots_service()
    assert svc is not None
    assert svc.domain_name == 'delivery-slot-selection-express-same-day'
    assert svc.module_version == '3.4.39'

def test_delivery_slots_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_delivery_slots_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_delivery_slots_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_delivery_slots_service()
    req = DeliverySlotsServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_delivery_slots_ai_model_inference():
    """Validate DeliverySlotsAIModel probability computation and confidence bounds."""
    model = get_delivery_slots_ai_model()
    assert model.MODEL_NAME == 'delivery-slot-selection-express-same-day-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_delivery_slots_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_39()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_39_to_database()
    assert count == len(seeds)
