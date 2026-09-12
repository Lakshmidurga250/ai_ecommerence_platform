"""
Layered Fraud Defense & Transaction Risk Engine.
Combines:
1. Deterministic Rule Engine (Card testing, coupon abuse, velocity spikes)
2. Statistical Velocity & Outlier Scoring
3. Unsupervised Isolation Forest Anomaly Detection
4. Human-in-the-loop review queue recommendations
"""

from typing import Dict, Any, List, Optional
import numpy as np
from ai.fraud.detector import FraudDetector


class LayeredFraudShield:
    def __init__(self):
        self.isolation_forest_detector = FraudDetector()

    def evaluate_order(
        self,
        order_amount: float,
        items_count: int,
        user_account_age_days: int,
        past_successful_orders: int,
        failed_attempts_last_hour: int = 0,
        coupon_applied: Optional[str] = None,
        coupon_used_by_ip_count: int = 1,
        user_avg_order_amount: float = 0.0,
        shipping_differs_from_billing: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a 3-layer transaction risk evaluation.
        Produces combined score (0-100), risk tier, triggered factors, and recommended action.
        """
        rule_violations = []
        rule_risk_penalty = 0.0

        # --- Layer 1: Deterministic Rules ---
        # Rule 1.1: Rapid failed payments (card testing attack)
        if failed_attempts_last_hour >= 3:
            rule_violations.append(f"High Velocity: {failed_attempts_last_hour} failed payment attempts in past hour")
            rule_risk_penalty += 35.0

        # Rule 1.2: High-value first transaction
        if past_successful_orders == 0 and user_account_age_days < 2 and order_amount > 500.0:
            rule_violations.append("New Account Alert: First order exceeds $500 threshold within 48h of registration")
            rule_risk_penalty += 25.0

        # Rule 1.3: Coupon abuse
        if coupon_applied and coupon_used_by_ip_count >= 3:
            rule_violations.append(f"Promo Abuse: Coupon '{coupon_applied}' claimed across {coupon_used_by_ip_count} accounts from same network")
            rule_risk_penalty += 20.0

        # Rule 1.4: Bulk purchase anomaly
        if items_count >= 12 and order_amount > 1200.0:
            rule_violations.append(f"Bulk Reseller Anomaly: Single order contains {items_count} units")
            rule_risk_penalty += 15.0

        # --- Layer 2: Statistical Deviation ---
        statistical_flags = []
        if user_avg_order_amount > 0 and past_successful_orders >= 3:
            ratio = order_amount / max(1.0, user_avg_order_amount)
            if ratio >= 4.0:
                statistical_flags.append(f"Order amount is {ratio:.1f}x higher than customer's established average (${user_avg_order_amount:.2f})")
                rule_risk_penalty += 20.0

        # --- Layer 3: Unsupervised Isolation Forest ML ---
        ml_eval = self.isolation_forest_detector.evaluate_transaction(
            order_amount=order_amount,
            items_count=items_count,
            days_since_signup=user_account_age_days,
            past_orders_count=past_successful_orders,
            failed_attempts_24h=failed_attempts_last_hour,
            user_avg_order_amount=user_avg_order_amount
        )

        ml_score = ml_eval["risk_score"]

        # Blend scores: 55% ML Anomaly + 45% Rule Penalties
        blended_risk = max(5.0, min(99.0, round((ml_score * 0.55) + (rule_risk_penalty * 0.45), 1)))

        all_factors = rule_violations + statistical_flags + [f for f in ml_eval.get("trigger_reasons", []) if f not in rule_violations]

        # Decision thresholds
        if blended_risk >= 75.0:
            decision = "HOLD_FOR_MANUAL_REVIEW"
            risk_tier = "CRITICAL"
            suggested_action = "Require billing verification before releasing order to warehouse"
        elif blended_risk >= 45.0:
            decision = "FLAG_FOR_MONITORING"
            risk_tier = "ELEVATED"
            suggested_action = "Post-fulfillment spot check recommended"
        else:
            decision = "APPROVE_AUTOMATICALLY"
            risk_tier = "LOW"
            suggested_action = "Clear order for automated fulfillment"

        return {
            "risk_score": blended_risk,
            "composite_risk_score": round(blended_risk / 100.0, 4),
            "risk_tier": risk_tier,
            "decision": decision,
            "suggested_action": suggested_action,
            "ml_anomaly_score": ml_score,
            "rule_penalty_score": min(100.0, rule_risk_penalty),
            "layer1_rule_triggers": rule_violations,
            "layer2_velocity_score": round(rule_risk_penalty / 100.0, 4),
            "layer3_anomaly_score": round(ml_score / 100.0, 4),
            "triggered_factors": all_factors
        }

    def evaluate_transaction(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience dictionary adapter for transaction risk scoring."""
        shipping_diff = False
        if "shipping_country" in txn and "billing_country" in txn:
            shipping_diff = (txn["shipping_country"] != txn["billing_country"])
            
        return self.evaluate_order(
            order_amount=float(txn.get("amount", txn.get("order_amount", 100.0))),
            items_count=int(txn.get("items_count", 1)),
            user_account_age_days=int(txn.get("user_account_age_days", txn.get("account_age_days", 30))),
            past_successful_orders=int(txn.get("past_successful_orders", txn.get("past_orders_count", 5))),
            failed_attempts_last_hour=int(txn.get("failed_attempts_last_hour", txn.get("card_declines_24h", 0))),
            coupon_applied=txn.get("coupon_applied"),
            user_avg_order_amount=float(txn.get("user_avg_order_amount", 0.0)),
            shipping_differs_from_billing=shipping_diff
        )

