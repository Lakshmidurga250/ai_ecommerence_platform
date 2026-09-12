"""
Loyalty & Customer Rewards API Router.
Provides customer loyalty tier metrics, points ledger, and reward coupon redemption.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.loyalty_service import LoyaltyService

router = APIRouter(prefix="/loyalty", tags=["Customer Loyalty & Rewards"])


class RedeemPointsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    points: int = Field(..., ge=1, description="Number of points to redeem (min 1)")


@router.get("/me")
def get_my_loyalty_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves current customer's loyalty points balance, tier level, and redemption options."""
    return LoyaltyService.get_loyalty_summary(db, current_user.id)


@router.post("/redeem")
def redeem_loyalty_points(
    payload: RedeemPointsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Redeems loyalty points for an instant discount coupon code."""
    return LoyaltyService.redeem_points_for_coupon(db, current_user.id, payload.points)
