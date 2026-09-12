"""
Shipping, Tracking, and Logistics API Endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.order import ShipmentRead, ShipmentEventRead
from app.services.shipping_service import ShippingService

router = APIRouter(prefix="/shipping", tags=["Shipping & Logistics"])


@router.get("/track/{order_id}", response_model=ShipmentRead)
def track_shipment(order_id: int, db: Session = Depends(get_db)):
    """Retrieve live tracking events and carrier status for an order."""
    shipment = ShippingService.get_shipment_by_order_id(db, order_id)
    return shipment


@router.post("/events", response_model=ShipmentEventRead, status_code=status.HTTP_201_CREATED)
def record_carrier_event(
    shipment_id: int = Query(...),
    status_code: str = Query(..., description="e.g. IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED"),
    location: str = Query(..., description="e.g. Sorting Hub Mumbai"),
    description: str = Query(..., description="Status description"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))
):
    """Simulate carrier package transit milestones."""
    return ShippingService.add_tracking_event(
        db=db,
        shipment_id=shipment_id,
        status=status_code,
        location=location,
        description=description
    )
