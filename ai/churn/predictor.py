"""
Customer Churn Prediction and Retention Intelligence Pipeline.
Models dormancy risk using recency decay, interaction drop-off, and engagement signals.
"""

from typing import Dict, Any, List, Optional
import numpy as np


class ChurnPredictor:
    @staticmethod
    def evaluate_churn_risk(
        days_since_last_purchase: int,
        total_orders: int,
        days_since_last_login: int,
        cart_abandonment_count: int,
        reviews_count: int,
        wishlist_count: int
    ) -> Dict[str, Any]:
        """
        Calculates mathematical churn probability using calibrated logistic sigmoid function:
        z = w1*recency + w2*login_gap + w3*abandonments - w4*orders - w5*reviews
        """
        # Feature weights calibrated on consumer retail dynamics
        z = (
            (days_since_last_purchase * 0.035) +
            (days_since_last_login * 0.040) +
            (cart_abandonment_count * 0.25) -
            (total_orders * 0.40) -
            (reviews_count * 0.30) -
            (wishlist_count * 0.15) - 0.8
        )

        churn_prob = 1.0 / (1.0 + np.exp(-z))
        churn_prob = max(0.02, min(0.98, round(float(churn_prob), 3)))

        contributing_factors = []
        if days_since_last_purchase > 45:
            contributing_factors.append(f"No purchases completed in the last {days_since_last_purchase} days")
        if days_since_last_login > 20:
            contributing_factors.append(f"Extended portal inactivity ({days_since_last_login} days since last session)")
        if cart_abandonment_count >= 2:
            contributing_factors.append(f"Detected {cart_abandonment_count} uncompleted cart checkout sessions")
        if total_orders <= 1:
            contributing_factors.append("Low lifetime historical purchase depth (1 order)")

        # Risk Classification & Retention Action
        if churn_prob >= 0.70:
            risk_category = "HIGH"
            retention_action = "Trigger high-priority re-engagement campaign: 15% discount coupon on saved wishlist items"
        elif churn_prob >= 0.40:
            risk_category = "MEDIUM"
            retention_action = "Send personalized product digest highlighting new arrivals in favorite categories"
        else:
            risk_category = "LOW"
            retention_action = "Maintain regular loyalty rewards and standard promotional notifications"

        return {
            "churn_probability": churn_prob,
            "risk_category": risk_category,
            "churn_risk_level": risk_category,
            "contributing_factors": contributing_factors or ["Normal engaged purchasing frequency"],
            "suggested_retention_action": retention_action
        }

    @classmethod
    def predict_churn(
        cls,
        recency_days: int = 30,
        purchase_count: int = 1,
        total_spend: float = 1000.0,
        days_since_last_purchase: Optional[int] = None,
        total_orders: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Alias for evaluate_churn_risk supporting named parameters from customer intelligence services.
        """
        days_p = days_since_last_purchase if days_since_last_purchase is not None else recency_days
        orders = total_orders if total_orders is not None else purchase_count
        return cls.evaluate_churn_risk(
            days_since_last_purchase=days_p,
            total_orders=orders,
            days_since_last_login=kwargs.get("days_since_last_login", 5),
            cart_abandonment_count=kwargs.get("cart_abandonment_count", 0),
            reviews_count=kwargs.get("reviews_count", 0),
            wishlist_count=kwargs.get("wishlist_count", 0)
        )
