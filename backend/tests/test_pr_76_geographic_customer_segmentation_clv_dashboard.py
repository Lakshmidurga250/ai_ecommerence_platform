"""
Pytest Test Suite for PR #76: geographic-customer-segmentation-clv-dashboard
Focus: Recency-Frequency-Monetary (RFM) 3D scoring grid, Champion/At-Risk segment categorizer
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.geographic_customer_segmentation_clv_dashboard import RfmSegmentationBiService, get_rfm_segmentation_bi_service, RfmSegmentationBiServiceRequest
from ai.geographic.geographic_customer_segmentation_clv_dashboard_ai_model import RfmSegmentationBiAIModel, get_rfm_segmentation_bi_ai_model
from database.seeds.geographic_customer_segmentation_clv_dashboard_seed import get_seed_data_pr_76, seed_pr_76_to_database

def test_rfm_segmentation_bi_service_initialization():
    """Verify RfmSegmentationBiService singleton instantiation and default attributes."""
    svc = get_rfm_segmentation_bi_service()
    assert svc is not None
    assert svc.domain_name == 'geographic-customer-segmentation-clv-dashboard'
    assert svc.module_version == '3.4.76'

def test_rfm_segmentation_bi_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_rfm_segmentation_bi_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_rfm_segmentation_bi_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_rfm_segmentation_bi_service()
    req = RfmSegmentationBiServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_rfm_segmentation_bi_ai_model_inference():
    """Validate RfmSegmentationBiAIModel probability computation and confidence bounds."""
    model = get_rfm_segmentation_bi_ai_model()
    assert model.MODEL_NAME == 'geographic-customer-segmentation-clv-dashboard-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_rfm_segmentation_bi_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_76()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_76_to_database()
    assert count == len(seeds)
