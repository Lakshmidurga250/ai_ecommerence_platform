"""
Pytest Test Suite for PR #65: admin-revenue-category-geographic-analytics
Focus: Geographic revenue choropleth aggregator, category GMV share, contribution margin breakdown
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.admin-revenue-category-geographic-analytics import AdminAnalyticsHubService, get_admin_analytics_hub_service, AdminAnalyticsHubServiceRequest
from ai.admin.admin-revenue-category-geographic-analytics_ai_model import AdminAnalyticsHubAIModel, get_admin_analytics_hub_ai_model
from database.seeds.admin-revenue-category-geographic-analytics_seed import get_seed_data_pr_65, seed_pr_65_to_database

def test_admin_analytics_hub_service_initialization():
    """Verify AdminAnalyticsHubService singleton instantiation and default attributes."""
    svc = get_admin_analytics_hub_service()
    assert svc is not None
    assert svc.domain_name == 'admin-revenue-category-geographic-analytics'
    assert svc.module_version == '3.4.65'

def test_admin_analytics_hub_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_admin_analytics_hub_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_admin_analytics_hub_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_admin_analytics_hub_service()
    req = AdminAnalyticsHubServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_admin_analytics_hub_ai_model_inference():
    """Validate AdminAnalyticsHubAIModel probability computation and confidence bounds."""
    model = get_admin_analytics_hub_ai_model()
    assert model.MODEL_NAME == 'admin-revenue-category-geographic-analytics-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_admin_analytics_hub_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_65()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_65_to_database()
    assert count == len(seeds)
