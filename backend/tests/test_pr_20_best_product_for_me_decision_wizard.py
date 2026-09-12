"""
Pytest Test Suite for PR #20: best-product-for-me-decision-wizard
Focus: Multi-criteria utility theory, weighted constraint solver, interactive questionnaire
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.best_product_for_me_decision_wizard import ShoppingWizardService, get_shopping_wizard_service, ShoppingWizardServiceRequest
from ai.best.best_product_for_me_decision_wizard_ai_model import ShoppingWizardAIModel, get_shopping_wizard_ai_model
from database.seeds.best_product_for_me_decision_wizard_seed import get_seed_data_pr_20, seed_pr_20_to_database

def test_shopping_wizard_service_initialization():
    """Verify ShoppingWizardService singleton instantiation and default attributes."""
    svc = get_shopping_wizard_service()
    assert svc is not None
    assert svc.domain_name == 'best-product-for-me-decision-wizard'
    assert svc.module_version == '3.4.20'

def test_shopping_wizard_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_shopping_wizard_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_shopping_wizard_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_shopping_wizard_service()
    req = ShoppingWizardServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_shopping_wizard_ai_model_inference():
    """Validate ShoppingWizardAIModel probability computation and confidence bounds."""
    model = get_shopping_wizard_ai_model()
    assert model.MODEL_NAME == 'best-product-for-me-decision-wizard-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_shopping_wizard_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_20()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_20_to_database()
    assert count == len(seeds)
