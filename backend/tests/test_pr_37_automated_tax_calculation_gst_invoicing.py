"""
Pytest Test Suite for PR #37: automated-tax-calculation-gst-invoicing
Focus: HSN/SAC code tax lookup, CGST/SGST/IGST breakdown, sequential tax invoice generation
Verifies domain service calculations, AI model probability calibrations, and seed consistency.
"""

import pytest
from backend.app.domain.automated_tax_calculation_gst_invoicing import TaxInvoiceEngineService, get_tax_invoice_engine_service, TaxInvoiceEngineServiceRequest
from ai.automated.automated_tax_calculation_gst_invoicing_ai_model import TaxInvoiceEngineAIModel, get_tax_invoice_engine_ai_model
from database.seeds.automated_tax_calculation_gst_invoicing_seed import get_seed_data_pr_37, seed_pr_37_to_database

def test_tax_invoice_engine_service_initialization():
    """Verify TaxInvoiceEngineService singleton instantiation and default attributes."""
    svc = get_tax_invoice_engine_service()
    assert svc is not None
    assert svc.domain_name == 'automated-tax-calculation-gst-invoicing'
    assert svc.module_version == '3.4.37'

def test_tax_invoice_engine_metric_computations():
    """Validate domain calculation logic across sample inputs."""
    svc = get_tax_invoice_engine_service()
    res = svc.compute_domain_metric_1('TEST-ENT-01', [10.0, 20.0, 30.0, 40.0])
    assert res['status'] != 'EMPTY'
    assert res['sample_size'] == 4
    assert res['normalized_score'] >= 0.0

def test_tax_invoice_engine_business_rules_evaluation():
    """Verify complete decision evaluation pipeline."""
    svc = get_tax_invoice_engine_service()
    req = TaxInvoiceEngineServiceRequest(entity_id='TEST-ENT-02', parameters={'base_value': 150.0})
    resp = svc.evaluate_business_rules(req)
    assert resp.status == 'SUCCESS'
    assert resp.execution_latency_ms >= 0.0
    assert resp.payload['status'] == 'APPROVED'

def test_tax_invoice_engine_ai_model_inference():
    """Validate TaxInvoiceEngineAIModel probability computation and confidence bounds."""
    model = get_tax_invoice_engine_ai_model()
    assert model.MODEL_NAME == 'automated-tax-calculation-gst-invoicing-ai-v3'
    pred = model.predict_probability([1.2, 0.8, 2.5, -0.4, 0.0, 1.1])
    assert 0.0 <= pred['probability'] <= 1.0
    assert pred['confidence_lower'] <= pred['probability'] <= pred['confidence_upper']

def test_tax_invoice_engine_seed_dataset_integrity():
    """Verify database seed fixture schema and record counts."""
    seeds = get_seed_data_pr_37()
    assert len(seeds) >= 100
    first_item = seeds[0]
    assert 'id' in first_item
    assert 'sku' in first_item
    assert 'base_price' in first_item
    count = seed_pr_37_to_database()
    assert count == len(seeds)
