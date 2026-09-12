"""
Customer Intelligence & 360 API Router.
Provides Customer 360 profiles, churn risk scoring, cohort analytics, and retention recommendations.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.services.customer_360_service import Customer360Service

router = APIRouter(prefix="/customer-intelligence", tags=["Customer Intelligence & 360"])


@router.get("/me/360")
def get_my_customer_360(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve personalized Customer 360 profile, spending metrics, and loyalty rewards for current user."""
    return Customer360Service.get_customer_360_profile(db, current_user.id)


@router.get("/users/{user_id}/360", dependencies=[Depends(RoleChecker(["ADMIN", "SELLER"]))])
def get_user_customer_360(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve full Customer 360 profile with churn prediction and retention actions (Admin/Seller only)."""
    return Customer360Service.get_customer_360_profile(db, user_id)
