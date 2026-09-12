"""
Behavioral Event Ingestion API Router.
Receives real-time user activity signals from the React frontend.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_optional_current_user, RoleChecker
from app.models.user import User
from app.services.event_tracking_service import EventTrackingService

router = APIRouter(prefix="/events", tags=["Event Tracking Platform"])


class EventTrackRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_type: str = Field(..., description="product_view, search, cart_add, wishlist_add, purchase, recommendation_click, etc.")
    session_id: Optional[str] = Field(None, description="Client session identifier")
    product_id: Optional[int] = Field(None, description="Related product ID")
    category_id: Optional[int] = Field(None, description="Related category ID")
    page_url: Optional[str] = Field(None, description="Current page URL")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom contextual metadata")


class BatchEventRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    events: List[EventTrackRequest]


@router.post("/track", status_code=status.HTTP_200_OK)
def track_event(
    payload: EventTrackRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Ingests a single customer behavioral event."""
    user_id = current_user.id if current_user else None
    ev_metadata = payload.metadata or {}
    if payload.page_url:
        ev_metadata["page_url"] = payload.page_url

    ev = EventTrackingService.record_event(
        db=db,
        event_type=payload.event_type,
        user_id=user_id,
        session_id=payload.session_id,
        product_id=payload.product_id,
        category_id=payload.category_id,
        metadata=ev_metadata
    )
    return {"status": "RECORDED", "event_id": ev.id, "event_type": ev.event_type}


@router.post("/batch", status_code=status.HTTP_200_OK)
def track_batch_events(
    payload: BatchEventRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Batch ingests client-side behavioral events."""
    user_id = current_user.id if current_user else None
    events_data = []
    for ev in payload.events:
        meta = ev.metadata or {}
        if ev.page_url:
            meta["page_url"] = ev.page_url
        events_data.append({
            "event_type": ev.event_type,
            "user_id": user_id,
            "session_id": ev.session_id,
            "product_id": ev.product_id,
            "category_id": ev.category_id,
            "metadata": meta
        })
    count = EventTrackingService.record_batch(db, events_data)
    return {"status": "RECORDED", "processed_count": count, "recorded_count": count}


@router.get("/summary", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def get_event_summary(db: Session = Depends(get_db)):
    """Retrieves operational event stream counts by type."""
    return EventTrackingService.get_event_metrics_summary(db)
