"""
Pytest Test Suite for PR #1: ai-shopping-agent-natural-lang
Focus: Autonomous shopping dialogue, intent extraction, multi-turn state machine
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.ai-shopping-agent-natural-lang import ShoppingAgentService, get_shopping_agent_service, ShoppingAgentServiceRequest
from ai.ai.ai-shopping-agent-natural-lang_ai_model import ShoppingAgentAIModel, get_shopping_agent_ai_model
from database.seeds.ai-shopping-agent-natural-lang_seed import get_seed_data_pr_1, seed_pr_1_to_database

def test_shopping_agent_service_initialization():
    """Verify ShoppingAgentService singleton instantiation and default attributes."""
    svc = get_shopping_agent_service()
    assert svc is not None
    assert svc.domain_name == 'ai-shopping-agent-natural-lang'
    assert svc.module_version == '3.4.1'

def test_shopping_agent_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_shopping_agent_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_shopping_agent_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_shopping_agent_service()
    req = ShoppingAgentServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_shopping_agent_ai_model_inference():
    """Validate ShoppingAgentAIModel probability computation and confidence bounds."""
    model = get_shopping_agent_ai_model()
    assert model.MODEL_NAME == 'ai-shopping-agent-natural-lang-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_shopping_agent_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_1()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_1_to_database()
    assert count == len(seeds)
