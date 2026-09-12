"""
Smart Logistics & Returns Intelligence API Router.
Provides proximity-based warehouse routing, delivery ETA predictions, and returns analytics.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.smart_logistics_service import SmartLogisticsService

router = APIRouter(prefix="/logistics", tags=["Smart Logistics & Returns"])


class RouteEstimateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: Optional[int] = Field(None, description="Optional target product ID")
    destination_pincode: Optional[str] = Field(None, description="Destination postal code")
    city: Optional[str] = Field(None, description="Destination delivery city e.g. Bengaluru, Mumbai, Delhi")
    state: Optional[str] = Field(None, description="Destination state")
    items: List[Dict[str, int]] = Field(default_factory=list, description="List of items with product_id and quantity")


@router.post("/estimate-delivery")
def estimate_delivery_route(
    payload: RouteEstimateRequest,
    db: Session = Depends(get_db)
):
    """Calculates optimal warehouse origin, carrier selection, and delivery ETA."""
    if payload.destination_pincode or payload.product_id:
        return SmartLogisticsService.estimate_route(
            db=db,
            product_id=payload.product_id or 1,
            destination_pincode=payload.destination_pincode or "560001"
        )
    return SmartLogisticsService.optimize_order_routing(
        db=db,
        destination_city=payload.city or "Bengaluru",
        destination_state=payload.state or "Karnataka",
        items=payload.items or []
    )


@router.get("/return-analytics")
def get_return_analytics(db: Session = Depends(get_db)):
    """Retrieves high-risk return products, reason distributions, and refund turnaround times."""
    return SmartLogisticsService.get_returns_analytics(db)
