"""
Fraud and Transaction Anomaly Detection Pipeline.
Combines Isolation Forest unsupervised anomaly scoring with deterministic risk attribution rules.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.ensemble import IsolationForest


class FraudDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_fitted = False
        # Baseline training distribution
        self._fit_baseline()

    def _fit_baseline(self):
        """Fit baseline normal transaction behavior."""
        # Features: [order_amount, items_count, days_since_signup, past_orders_count, failed_attempts_24h]
        np.random.seed(42)
        normal_data = np.column_stack([
            np.random.normal(loc=1800, scale=800, size=500),      # Typical order amount
            np.random.poisson(lam=2.5, size=500),                  # Typical item count
            np.random.exponential(scale=120, size=500),            # Account age (days)
            np.random.poisson(lam=4.0, size=500),                  # Past orders count
            np.random.choice([0, 0, 0, 0, 1], size=500)            # Failed attempts
        ])
        normal_data = np.clip(normal_data, a_min=0, a_max=None)
        self.model.fit(normal_data)
        self.is_fitted = True

    def evaluate_transaction(
        self,
        order_amount: float,
        items_count: int,
        days_since_signup: int,
        past_orders_count: int,
        failed_attempts_24h: int = 0,
        user_avg_order_amount: float = 0.0
    ) -> Dict[str, Any]:
        """
        Evaluates a transaction for anomalous patterns.
        Produces a risk score (0 to 100), risk level, and transparent trigger reasons.
        """
        features = np.array([[
            order_amount,
            items_count,
            days_since_signup,
            past_orders_count,
            failed_attempts_24h
        ]])

        # Isolation Forest decision function: negative values indicate outliers
        anomaly_score = self.model.decision_function(features)[0]  # typically -0.5 to +0.5
        # Transform to 0-100 scale (lower decision function = higher anomaly risk)
        normalized_risk = max(5.0, min(95.0, round((0.3 - anomaly_score) * 100.0, 1)))

        trigger_reasons: List[str] = []

        # Deterministic risk indicators
        if user_avg_order_amount > 0 and order_amount > (user_avg_order_amount * 3.5):
            normalized_risk = min(98.0, normalized_risk + 25.0)
            trigger_reasons.append(f"Order amount (₹{order_amount:.0f}) is > 3.5x higher than user average (₹{user_avg_order_amount:.0f})")

        if failed_attempts_24h >= 3:
            normalized_risk = min(98.0, normalized_risk + 30.0)
            trigger_reasons.append(f"Detected {failed_attempts_24h} consecutive failed payment attempts within 24 hours")

        if days_since_signup < 2 and order_amount > 15000:
            normalized_risk = min(98.0, normalized_risk + 20.0)
            trigger_reasons.append("High-value first transaction on newly created account (< 48 hours)")

        if items_count >= 15:
            normalized_risk = min(98.0, normalized_risk + 10.0)
            trigger_reasons.append(f"Unusually high single-order item quantity ({items_count} units)")

        # Risk Classification
        if normalized_risk >= 75.0:
            level = "CRITICAL"
            suggested_action = "Manual risk review required prior to shipment dispatch"
        elif normalized_risk >= 55.0:
            level = "HIGH"
            suggested_action = "Suspicious activity detected — review recommended"
        elif normalized_risk >= 35.0:
            level = "MEDIUM"
            suggested_action = "Standard verification check"
        else:
            level = "LOW"
            suggested_action = "Standard automated processing"

        is_suspicious = (level in ("HIGH", "CRITICAL"))

        return {
            "risk_score": round(normalized_risk, 1),
            "risk_level": level,
            "is_suspicious": is_suspicious,
            "trigger_reasons": trigger_reasons,
            "suggested_action": suggested_action
        }


# Global Fraud Detector Instance
fraud_detector = FraudDetector()
