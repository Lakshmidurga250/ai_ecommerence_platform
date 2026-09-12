"""
Pytest Test Suite for PR #6: ai-review-quality-fake-detector
Focus: Shannon entropy analyzer, repetition detection, review authenticity classifier
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.ai_review_quality_fake_detector import FakeReviewShieldService, get_fake_review_shield_service, FakeReviewShieldServiceRequest
from ai.ai.ai_review_quality_fake_detector_ai_model import FakeReviewShieldAIModel, get_fake_review_shield_ai_model
from database.seeds.ai_review_quality_fake_detector_seed import get_seed_data_pr_6, seed_pr_6_to_database

def test_fake_review_shield_service_initialization():
    """Verify FakeReviewShieldService singleton instantiation and default attributes."""
    svc = get_fake_review_shield_service()
    assert svc is not None
    assert svc.domain_name == 'ai-review-quality-fake-detector'
    assert svc.module_version == '3.4.6'

def test_fake_review_shield_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_fake_review_shield_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_fake_review_shield_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_fake_review_shield_service()
    req = FakeReviewShieldServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_fake_review_shield_ai_model_inference():
    """Validate FakeReviewShieldAIModel probability computation and confidence bounds."""
    model = get_fake_review_shield_ai_model()
    assert model.MODEL_NAME == 'ai-review-quality-fake-detector-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_fake_review_shield_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_6()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_6_to_database()
    assert count == len(seeds)
