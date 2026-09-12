"""
Inventory Intelligence & Multi-Horizon Demand Forecasting API Router.
Provides ABC/XYZ classification, warehouse stock transfers, and multi-horizon demand projections.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from ai.inventory_intelligence.abc_xyz_analyzer import ABCXYZAnalyzer
from ai.forecasting.forecaster import DemandForecaster

router = APIRouter(prefix="/inventory-intelligence", tags=["Inventory Intelligence"])


@router.get("/matrix")
def get_inventory_abc_xyz_matrix(
    format: Optional[str] = Query("list", description="'list' or 'summary'"),
    db: Session = Depends(get_db)
):
    """Computes network-wide ABC/XYZ inventory matrix and stockout/dead-stock risks."""
    summary = ABCXYZAnalyzer.compute_abc_xyz_matrix(db)
    if format == "summary":
        return summary
    # Return formatted list for table/grid
    analyzer = ABCXYZAnalyzer(db)
    return analyzer.generate_matrix()


@router.get("/transfers")
def get_warehouse_transfer_recommendations(db: Session = Depends(get_db)):
    """Retrieves smart inter-warehouse stock rebalancing transfer recommendations."""
    analyzer = ABCXYZAnalyzer(db)
    return analyzer.recommend_transfers()


@router.get("/multi-horizon-forecast/{product_id}")
def get_multi_horizon_forecast(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Computes 7-day, 14-day, 30-day, and 90-day future demand forecasts with confidence bounds
    and stockout risk probability.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    daily_sales = max(1.0, (product.sales_count or 10) / 60.0)

    # Multi-horizon projections
    h7 = round(daily_sales * 7, 1)
    h14 = round(daily_sales * 14, 1)
    h30 = round(daily_sales * 30, 1)
    h90 = round(daily_sales * 90, 1)

    stockout_days = int(product.stock / daily_sales) if daily_sales > 0 else 999
    stockout_risk = "HIGH" if stockout_days <= 14 else ("MEDIUM" if stockout_days <= 30 else "LOW")

    horizons_dict = {
        "day_7": {"predicted_units": h7, "lower_bound": round(h7 * 0.85, 1), "upper_bound": round(h7 * 1.20, 1)},
        "day_14": {"predicted_units": h14, "lower_bound": round(h14 * 0.82, 1), "upper_bound": round(h14 * 1.25, 1)},
        "day_30": {"predicted_units": h30, "lower_bound": round(h30 * 0.80, 1), "upper_bound": round(h30 * 1.30, 1)},
        "day_90": {"predicted_units": h90, "lower_bound": round(h90 * 0.75, 1), "upper_bound": round(h90 * 1.40, 1)}
    }

    return {
        "product_id": product.id,
        "product_name": product.name,
        "current_stock": product.stock,
        "historical_sales_velocity": round(daily_sales, 2),
        "stockout_days": stockout_days,
        "stockout_risk": stockout_risk,
        "horizons": horizons_dict,
        "forecasts": horizons_dict
    }
