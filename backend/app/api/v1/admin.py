"""
Administrative Management & Moderation API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from app.models.user import User
from app.models.seller import Seller
from app.models.analytics import FraudAlert
from app.models.audit import AuditLog
from app.schemas.user import UserRead
from app.schemas.seller import SellerRead, SellerStatusUpdate
from app.schemas.analytics import AuditLogRead
from app.schemas.ai import FraudRiskEvaluation
from app.services.seller_service import SellerService

router = APIRouter(prefix="/admin", tags=["Administrative Control"])


@router.get("/users", response_model=List[UserRead])
def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """List all registered platform users."""
    return db.query(User).offset(skip).limit(limit).all()


@router.patch("/sellers/{seller_id}/status", response_model=SellerRead)
def update_seller_approval_status(
    seller_id: int,
    data: SellerStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Approve, suspend, or reject a seller store."""
    return SellerService.update_seller_status(db, seller_id, data.status)


@router.get("/fraud-alerts")
def list_fraud_alerts(
    status: Optional[str] = Query(None, description="PENDING_REVIEW, APPROVED, BLOCKED"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """List transactions flagged for fraud or anomaly review."""
    q = db.query(FraudAlert)
    if status:
        q = q.filter(FraudAlert.status == status)
    return q.order_by(FraudAlert.created_at.desc()).all()


@router.patch("/fraud-alerts/{alert_id}/review")
def review_fraud_alert(
    alert_id: int,
    action: str = Query(..., pattern="^(APPROVED|BLOCKED)$"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Review and resolve a flagged fraud alert."""
    from datetime import datetime, timezone
    from app.core.exceptions import NotFoundException
    alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()
    if not alert:
        raise NotFoundException("FraudAlert", str(alert_id))
    alert.status = action
    alert.reviewed_by = admin_user.id
    alert.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/audit-logs", response_model=List[AuditLogRead])
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Retrieve immutable audit log trail for security and financial actions."""
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
