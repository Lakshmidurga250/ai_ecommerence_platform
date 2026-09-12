"""
Inventory Replenishment & Stock Intelligence Engine.
Computes Safety Stock, Reorder Point (ROP), Economic Order Quantity (EOQ),
and detects overstock/dead-stock risks using actual sales velocity.
"""

import math
from typing import Dict, Any, List, Optional
import numpy as np


class InventoryIntelligenceEngine:

    @staticmethod
    def calculate_reorder_parameters(
        daily_sales_history: List[int],
        lead_time_days: int = 5,
        service_level: float = 0.95,
        ordering_cost: float = 50.0,
        unit_cost: float = 100.0,
        holding_cost_rate: float = 0.20
    ) -> Dict[str, Any]:
        """
        Calculates mathematical inventory parameters:
        - Mean Daily Demand & Demand Standard Deviation
        - Safety Stock (SS) = Z * std_dev * sqrt(lead_time)
        - Reorder Point (ROP) = (mean_demand * lead_time) + SS
        - Economic Order Quantity (EOQ) = sqrt(2 * D * S / H)
        """
        if not daily_sales_history:
            daily_sales_history = [1, 2, 1, 3, 2]

        data = np.array(daily_sales_history)
        mean_demand = float(np.mean(data))
        std_demand = float(np.std(data)) if len(data) > 1 else max(0.5, mean_demand * 0.3)

        # Service level Z-score mapping
        z_scores = {
            0.90: 1.28,
            0.95: 1.65,
            0.98: 2.05,
            0.99: 2.33
        }
        z = z_scores.get(service_level, 1.65)

        safety_stock = int(math.ceil(z * std_demand * math.sqrt(lead_time_days)))
        lead_time_demand = mean_demand * lead_time_days
        reorder_point = int(math.ceil(lead_time_demand + safety_stock))

        # EOQ calculation
        annual_demand = max(10, mean_demand * 365.0)
        holding_cost_per_unit = max(1.0, unit_cost * holding_cost_rate)
        eoq = int(math.ceil(math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)))

        return {
            "mean_daily_demand": round(mean_demand, 2),
            "std_daily_demand": round(std_demand, 2),
            "lead_time_days": lead_time_days,
            "service_level": service_level,
            "safety_stock_units": safety_stock,
            "reorder_point_units": reorder_point,
            "economic_order_quantity_units": eoq,
            "annual_demand_projected": int(round(annual_demand))
        }

    @staticmethod
    def evaluate_product_inventory(
        current_stock: int,
        daily_sales_history: List[int],
        lead_time_days: int = 5,
        days_since_last_sale: int = 0
    ) -> Dict[str, Any]:
        """
        Evaluates current inventory status for reorder urgency, overstock, or dead-stock risk.
        """
        params = InventoryIntelligenceEngine.calculate_reorder_parameters(
            daily_sales_history=daily_sales_history,
            lead_time_days=lead_time_days
        )

        rop = params["reorder_point_units"]
        safety_stock = params["safety_stock_units"]
        mean_demand = max(0.1, params["mean_daily_demand"])

        days_of_supply = round(current_stock / mean_demand, 1)

        # Classify status
        if current_stock <= 0:
            stock_status = "OUT_OF_STOCK"
            urgency = "CRITICAL"
            recommended_order = params["economic_order_quantity_units"]
        elif current_stock <= rop:
            stock_status = "REORDER_NOW"
            urgency = "HIGH"
            recommended_order = max(params["economic_order_quantity_units"], rop - current_stock + safety_stock)
        elif days_since_last_sale >= 60 and current_stock > 10:
            stock_status = "DEAD_STOCK_RISK"
            urgency = "LOW"
            recommended_order = 0
        elif days_of_supply > 120:
            stock_status = "OVERSTOCKED"
            urgency = "LOW"
            recommended_order = 0
        else:
            stock_status = "HEALTHY"
            urgency = "NONE"
            recommended_order = 0

        return {
            "current_stock": current_stock,
            "stock_status": stock_status,
            "urgency": urgency,
            "days_of_supply": days_of_supply,
            "reorder_point": rop,
            "safety_stock": safety_stock,
            "recommended_reorder_units": recommended_order,
            "days_since_last_sale": days_since_last_sale
        }
