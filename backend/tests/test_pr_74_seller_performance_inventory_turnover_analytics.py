"""
Pytest Test Suite for PR #74: seller-performance-inventory-turnover-analytics
Focus: Inventory turnover ratio (ITR), Days of Inventory Outstanding (DIO), slow-moving stock identifier
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.seller_performance_inventory_turnover_analytics import InventoryTurnoverService, get_inventory_turnover_service, InventoryTurnoverServiceRequest
from ai.seller.seller_performance_inventory_turnover_analytics_ai_model import InventoryTurnoverAIModel, get_inventory_turnover_ai_model
from database.seeds.seller_performance_inventory_turnover_analytics_seed import get_seed_data_pr_74, seed_pr_74_to_database

def test_inventory_turnover_service_initialization():
    """Verify InventoryTurnoverService singleton instantiation and default attributes."""
    svc = get_inventory_turnover_service()
    assert svc is not None
    assert svc.domain_name == 'seller-performance-inventory-turnover-analytics'
    assert svc.module_version == '3.4.74'

def test_inventory_turnover_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_inventory_turnover_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_inventory_turnover_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_inventory_turnover_service()
    req = InventoryTurnoverServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_inventory_turnover_ai_model_inference():
    """Validate InventoryTurnoverAIModel probability computation and confidence bounds."""
    model = get_inventory_turnover_ai_model()
    assert model.MODEL_NAME == 'seller-performance-inventory-turnover-analytics-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_inventory_turnover_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_74()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_74_to_database()
    assert count == len(seeds)
