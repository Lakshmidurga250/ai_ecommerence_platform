"""
Promotion & Discount Optimization Engine.
Simulates demand response curves, price elasticity of demand, gross margins, and volume lifts
across discrete promotional discount tiers to identify profit-maximizing and revenue-maximizing promotions.
"""
from typing import Dict, Any, List, Optional
import math
try:
    from app.models.product import Product
except ImportError:
    from backend.app.models.product import Product


class PromotionOptimizer:
    """
    Simulates promotional campaign economics and predicts optimal discount levels.
    """

    DEFAULT_DISCOUNT_TIERS = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0]

    # Category baseline price elasticities (absolute values)
    CATEGORY_ELASTICITIES = {
        "laptops-computing": 1.25,
        "smartphones-tablets": 1.40,
        "audio-wearables": 1.65,
        "footwear-running": 1.85,
        "athletic-apparel": 1.95,
        "gaming-accessories": 1.55,
        "home-kitchen": 1.35,
        "personal-care-grooming": 1.70,
        "books-stationery": 1.10,
    }

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def optimize_promotion(
        self,
        product_id: int,
        unit_cost_estimate: Optional[float] = None,
        baseline_weekly_sales: int = 25,
        target_objective: str = "MAX_PROFIT",  # MAX_PROFIT or MAX_REVENUE
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Simulates all discount tiers for a product and determines the mathematically optimal promotion.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"error": f"Product {product_id} not found"}

        current_price = product.price
        category_slug = product.category.slug if product.category else "general"
        elasticity = self.CATEGORY_ELASTICITIES.get(category_slug, 1.50)

        # If cost is not provided, estimate unit cost at 65% of MRP (35% baseline margin)
        unit_cost = unit_cost_estimate if unit_cost_estimate is not None else round(current_price * 0.65, 2)
        baseline_margin_per_unit = current_price - unit_cost

        tier_simulations = []
        best_profit_tier = None
        best_profit_val = -float("inf")
        best_revenue_tier = None
        best_revenue_val = -float("inf")

        for discount_pct in self.DEFAULT_DISCOUNT_TIERS:
            discount_ratio = discount_pct / 100.0
            discounted_price = round(current_price * (1.0 - discount_ratio), 2)
            margin_per_unit = round(discounted_price - unit_cost, 2)

            # Demand shift calculation: Delta Q / Q = - elasticity * (Delta P / P)
            # Since Delta P is negative (price drop), quantity increases
            price_change_ratio = -discount_ratio
            volume_lift_pct = round(abs(elasticity * price_change_ratio) * 100.0, 2)
            predicted_quantity = round(baseline_weekly_sales * (1.0 + (volume_lift_pct / 100.0)), 1)

            projected_revenue = round(discounted_price * predicted_quantity, 2)
            projected_profit = round(margin_per_unit * predicted_quantity, 2)
            margin_percentage = round((margin_per_unit / max(0.01, discounted_price)) * 100.0, 1)

            # Breakeven volume lift required to maintain total profit:
            # (P0 - C) * Q0 = (P_new - C) * Q_be ==> Q_be / Q0 = (P0 - C) / (P_new - C)
            if margin_per_unit > 0:
                breakeven_lift_pct = round(((baseline_margin_per_unit / margin_per_unit) - 1.0) * 100.0, 1)
            else:
                breakeven_lift_pct = 999.9

            simulation_point = {
                "discount_pct": discount_pct,
                "discounted_price": discounted_price,
                "margin_per_unit": margin_per_unit,
                "margin_percentage": margin_percentage,
                "volume_lift_pct": volume_lift_pct,
                "predicted_quantity": predicted_quantity,
                "projected_revenue": projected_revenue,
                "projected_profit": projected_profit,
                "breakeven_lift_pct": breakeven_lift_pct,
                "is_profitable": margin_per_unit > 0
            }
            tier_simulations.append(simulation_point)

            if projected_profit > best_profit_val and margin_per_unit > 0:
                best_profit_val = projected_profit
                best_profit_tier = simulation_point

            if projected_revenue > best_revenue_val:
                best_revenue_val = projected_revenue
                best_revenue_tier = simulation_point

        recommended_tier = best_profit_tier if target_objective == "MAX_PROFIT" else best_revenue_tier

        return {
            "product_id": product.id,
            "product_name": product.name,
            "category": category_slug,
            "current_price": current_price,
            "estimated_unit_cost": unit_cost,
            "baseline_weekly_sales": baseline_weekly_sales,
            "elasticity_coefficient": elasticity,
            "target_objective": target_objective,
            "recommended_promotion": {
                "optimal_discount_pct": recommended_tier["discount_pct"] if recommended_tier else 0.0,
                "promotional_price": recommended_tier["discounted_price"] if recommended_tier else current_price,
                "expected_volume_lift": f"+{recommended_tier['volume_lift_pct']}%" if recommended_tier else "+0%",
                "expected_weekly_revenue": recommended_tier["projected_revenue"] if recommended_tier else 0.0,
                "expected_weekly_profit": recommended_tier["projected_profit"] if recommended_tier else 0.0,
                "profit_lift_pct": round(((recommended_tier["projected_profit"] / max(1.0, baseline_weekly_sales * baseline_margin_per_unit)) - 1.0) * 100.0, 1) if recommended_tier else 0.0,
                "recommendation_summary": (
                    f"Offer a {recommended_tier['discount_pct']}% promotion (₹{recommended_tier['discounted_price']}). "
                    f"Elasticity of {elasticity} will drive a +{recommended_tier['volume_lift_pct']}% volume lift, "
                    f"maximizing weekly net profit to ₹{recommended_tier['projected_profit']}."
                ) if recommended_tier else "Keep at baseline pricing."
            },
            "all_tier_simulations": tier_simulations
        }
