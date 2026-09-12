"""
Customer Lifetime Value (CLV) & Behavioral Cohort Analysis Engine.
Calculates historical & predictive customer lifetime value,
segments customers into actionable retail cohorts, and generates tailored retention actions.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import numpy as np


class CustomerIntelligenceEngine:

    @staticmethod
    def calculate_clv(
        historical_spend: float,
        order_count: int,
        days_active: int,
        gross_margin: float = 0.35,
        discount_rate_annual: float = 0.10
    ) -> Dict[str, Any]:
        """
        Calculates Historical CLV and Forward-Looking Predictive CLV.
        Formula:
        Historical CLV = Cumulative Margin = Spend * Gross Margin
        Predictive CLV = (AOV * Annual Frequency * Gross Margin) / (Churn Rate + Discount Rate)
        """
        if order_count == 0 or days_active <= 0:
            return {
                "historical_clv": 0.0,
                "predictive_clv_1yr": 0.0,
                "aov": 0.0,
                "annual_order_frequency": 0.0,
                "customer_tier": "PROSPECT"
            }

        aov = round(historical_spend / max(1, order_count), 2)
        annual_order_frequency = round((order_count / max(1.0, days_active)) * 365.0, 2)

        historical_margin = round(historical_spend * gross_margin, 2)

        # Estimate churn probability inversely proportional to frequency
        estimated_churn = max(0.08, min(0.60, round(1.0 / (1.0 + np.log1p(order_count)), 3)))
        denom = max(0.05, estimated_churn + discount_rate_annual)

        expected_annual_margin = (aov * annual_order_frequency) * gross_margin
        predictive_clv_1yr = round(expected_annual_margin / denom, 2)

        # Tier assignment
        if historical_spend >= 2500 or predictive_clv_1yr >= 4000:
            tier = "VIP_PLATINUM"
        elif historical_spend >= 1000 or predictive_clv_1yr >= 1800:
            tier = "LOYAL_GOLD"
        elif historical_spend >= 300 or predictive_clv_1yr >= 600:
            tier = "GROWING_SILVER"
        else:
            tier = "BRONZE_EXPLORER"

        return {
            "historical_clv": historical_margin,
            "predictive_clv_1yr": predictive_clv_1yr,
            "aov": aov,
            "annual_order_frequency": annual_order_frequency,
            "customer_tier": tier,
            "estimated_churn_rate": estimated_churn
        }

    @staticmethod
    def assign_cohort(
        days_since_signup: int,
        days_since_last_order: Optional[int],
        order_count: int,
        total_spend: float
    ) -> Dict[str, Any]:
        """
        Assigns customer to a dynamic behavioral cohort and returns strategic retention playbooks.
        """
        if order_count == 0:
            if days_since_signup <= 14:
                cohort = "NEW_UNACTIVATED"
                strategy = "Send welcome onboarding sequence with first-order discount code"
            else:
                cohort = "ABANDONED_LEAD"
                strategy = "Re-engage with personalized trending product recommendations"
        elif days_since_last_order is not None and days_since_last_order <= 30:
            if total_spend >= 1000 or order_count >= 3:
                cohort = "CHAMPION_LOYALIST"
                strategy = "Invite to exclusive VIP previews and priority customer support"
            else:
                cohort = "ACTIVE_RECENT"
                strategy = "Encourage cross-category discovery with bundle discounts"
        elif days_since_last_order is not None and 30 < days_since_last_order <= 90:
            if total_spend >= 500:
                cohort = "AT_RISK_HIGH_VALUE"
                strategy = "High-priority outreach: targeted incentive or survey from customer success"
            else:
                cohort = "COOLING_DOWN"
                strategy = "Send automated re-activation newsletter with new arrivals in favorite categories"
        else:
            cohort = "DORMANT_CHURNED"
            strategy = "Win-back campaign with special limited-time promo code"

        return {
            "cohort": cohort,
            "recommended_strategy": strategy,
            "days_since_signup": days_since_signup,
            "days_since_last_order": days_since_last_order,
            "total_spend": total_spend,
            "order_count": order_count
        }

    @staticmethod
    def analyze_customer_base(customer_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates cohort distribution and average metrics across the entire platform."""
        cohort_counts = {}
        total_clv = 0.0
        total_spend = 0.0

        for p in customer_profiles:
            cohort_data = CustomerIntelligenceEngine.assign_cohort(
                days_since_signup=p.get("days_since_signup", 30),
                days_since_last_order=p.get("days_since_last_order"),
                order_count=p.get("order_count", 0),
                total_spend=p.get("total_spend", 0.0)
            )
            c = cohort_data["cohort"]
            cohort_counts[c] = cohort_counts.get(c, 0) + 1

            clv_data = CustomerIntelligenceEngine.calculate_clv(
                historical_spend=p.get("total_spend", 0.0),
                order_count=p.get("order_count", 0),
                days_active=p.get("days_since_signup", 30)
            )
            total_clv += clv_data["predictive_clv_1yr"]
            total_spend += p.get("total_spend", 0.0)

        n = max(1, len(customer_profiles))
        return {
            "total_customers_analyzed": len(customer_profiles),
            "cohort_distribution": cohort_counts,
            "average_predictive_clv": round(total_clv / n, 2),
            "average_spend": round(total_spend / n, 2)
        }
