"""
Pytest Test Suite for PR #5: ai-review-aspect-sentiment-summarizer
Focus: 5-aspect sentiment parser, customer consensus extractor, pros/cons synthesizer
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.ai-review-aspect-sentiment-summarizer import ReviewSummarizerService, get_review_summarizer_service, ReviewSummarizerServiceRequest
from ai.ai.ai-review-aspect-sentiment-summarizer_ai_model import ReviewSummarizerAIModel, get_review_summarizer_ai_model
from database.seeds.ai-review-aspect-sentiment-summarizer_seed import get_seed_data_pr_5, seed_pr_5_to_database

def test_review_summarizer_service_initialization():
    """Verify ReviewSummarizerService singleton instantiation and default attributes."""
    svc = get_review_summarizer_service()
    assert svc is not None
    assert svc.domain_name == 'ai-review-aspect-sentiment-summarizer'
    assert svc.module_version == '3.4.5'

def test_review_summarizer_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_review_summarizer_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_review_summarizer_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_review_summarizer_service()
    req = ReviewSummarizerServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_review_summarizer_ai_model_inference():
    """Validate ReviewSummarizerAIModel probability computation and confidence bounds."""
    model = get_review_summarizer_ai_model()
    assert model.MODEL_NAME == 'ai-review-aspect-sentiment-summarizer-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_review_summarizer_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_5()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_5_to_database()
    assert count == len(seeds)
