"""
Analytics & Behavioral Event Logging API Endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_optional_current_user, RoleChecker
from app.models.user import User
from app.schemas.analytics import BusinessOverviewMetrics, BehaviorEventCreate
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=BusinessOverviewMetrics)
def get_business_overview(
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Retrieve platform-wide operational business metrics."""
    return AnalyticsService.get_business_overview(db)


@router.post("/event", status_code=status.HTTP_201_CREATED)
def record_event(
    data: BehaviorEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_current_user)
):
    """Record customer interaction events (views, clicks, cart adds) to feed the AI pipeline."""
    user_id = current_user.id if current_user else None
    AnalyticsService.record_behavior_event(
        db=db,
        event_type=data.event_type,
        user_id=user_id,
        product_id=data.product_id,
        category_id=data.category_id,
        session_id=data.session_id,
        metadata=data.metadata
    )
    return {"status": "recorded"}
