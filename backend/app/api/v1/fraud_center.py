"""
Fraud Center API Router.
Provides administrative alert triage, explainable risk decomposition, and transaction blocking.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.services.fraud_intelligence_service import FraudIntelligenceService

router = APIRouter(prefix="/fraud", tags=["Fraud Intelligence Center"])


class ResolveAlertRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action: Optional[str] = Field(None, description="Resolution: APPROVE, BLOCK, or FALSE_POSITIVE")
    resolution: Optional[str] = Field(None, description="Alias for action: APPROVED or BLOCKED")
    notes: Optional[str] = Field(None, description="Admin investigation notes")


@router.get("/alerts", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def get_fraud_alerts(
    status: Optional[str] = Query(None, description="Filter by status: PENDING_REVIEW, APPROVED, BLOCKED"),
    risk_level: Optional[str] = Query(None, description="Filter by risk: LOW, MEDIUM, HIGH, CRITICAL"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieves paginated fraud security alerts for administrative review."""
    res = FraudIntelligenceService.list_alerts(db, status=status, risk_level=risk_level, skip=skip, limit=limit)
    return res.get("alerts", [])


@router.post("/alerts/{alert_id}/resolve", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def resolve_fraud_alert(
    alert_id: int,
    payload: ResolveAlertRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Executes administrative action on a flagged fraud alert."""
    action = payload.action or payload.resolution or "APPROVE"
    return FraudIntelligenceService.resolve_alert(
        db=db,
        alert_id=alert_id,
        admin_user_id=admin.id,
        action=action,
        resolution_notes=payload.notes
    )



@router.get("/statistics", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def get_fraud_statistics(db: Session = Depends(get_db)):
    """Retrieves high-level fraud prevention metrics and risk tier distribution."""
    return FraudIntelligenceService.get_fraud_statistics(db)
