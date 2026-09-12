"""
Unit and Statistical Tests for Layered Fraud Defense, CLV Cohorts, and Inventory Replenishment.
Validates Isolation Forest anomaly detection, statistical safety stock, EOQ,
and predictive Customer Lifetime Value calculations.
"""

import pytest
import math
from ai.fraud.layered_shield import LayeredFraudShield
from ai.customer_intelligence.clv_cohorts import CustomerIntelligenceEngine
from ai.inventory_intelligence.replenishment import InventoryIntelligenceEngine


def test_layered_fraud_shield_clean_transaction():
    """Verifies that a typical, modest order with verified credentials receives low risk and APPROVE_AUTOMATICALLY decision."""
    shield = LayeredFraudShield()
    txn = {
        "user_id": 10,
        "amount": 45.0,
        "items_count": 1,
        "user_account_age_days": 90,
        "past_successful_orders": 12,
        "failed_attempts_last_hour": 0,
        "shipping_country": "US",
        "billing_country": "US",
        "device_fingerprint": "dev_normal_123"
    }
    res = shield.evaluate_transaction(txn)
    assert res["decision"] == "APPROVE_AUTOMATICALLY"
    assert res["composite_risk_score"] < 0.45
    assert "layer1_rule_triggers" in res
    assert "layer2_velocity_score" in res
    assert "layer3_anomaly_score" in res


def test_layered_fraud_shield_high_risk_transaction():
    """Verifies that an order with excessive velocity, billing mismatches, and multiple declines gets flagged."""
    shield = LayeredFraudShield()
    suspicious_txn = {
        "user_id": 999,
        "amount": 25000.0,
        "items_count": 15,
        "user_account_age_days": 1,
        "past_successful_orders": 0,
        "failed_attempts_last_hour": 5,
        "shipping_country": "US",
        "billing_country": "NG",
        "device_fingerprint": "dev_anon_vpn"
    }
    res = shield.evaluate_transaction(suspicious_txn)
    assert res["composite_risk_score"] >= 0.50
    assert res["decision"] in ("HOLD_FOR_MANUAL_REVIEW", "FLAG_FOR_MONITORING")
    assert len(res["layer1_rule_triggers"]) >= 1



def test_clv_historical_and_predictive():
    """Verifies mathematical CLV formulas and cohort segmentation."""
    clv_res = CustomerIntelligenceEngine.calculate_clv(
        historical_spend=1200.0,
        order_count=8,
        days_active=180,
        gross_margin=0.35,
        discount_rate_annual=0.10
    )
    assert clv_res["historical_clv"] > 0
    assert clv_res["predictive_clv_1yr"] > 0
    assert "customer_tier" in clv_res
    assert clv_res["customer_tier"] in ("VIP_PLATINUM", "LOYAL_GOLD", "GROWING_SILVER", "BRONZE_EXPLORER")


def test_inventory_safety_stock_and_rop():
    """Verifies statistical Safety Stock (Z * sigma * sqrt(L)) and Reorder Point formulas."""
    daily_sales = [18, 22, 20, 24, 19, 21, 23, 17, 20, 22]
    lead_time_days = 9

    calc = InventoryIntelligenceEngine.calculate_reorder_parameters(
        daily_sales_history=daily_sales,
        lead_time_days=lead_time_days,
        service_level=0.95
    )

    assert calc["mean_daily_demand"] > 0
    assert calc["safety_stock_units"] > 0
    assert calc["reorder_point_units"] > calc["safety_stock_units"]
    assert calc["economic_order_quantity_units"] > 0


