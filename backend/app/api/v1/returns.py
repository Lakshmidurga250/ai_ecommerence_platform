"""
Order Returns & Refund Management API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.models.order import Return
from app.schemas.order import ReturnRequestCreate, ReturnRead
from app.services.return_service import ReturnService

router = APIRouter(prefix="/returns", tags=["Returns & Refunds"])


@router.post("/", response_model=ReturnRead, status_code=status.HTTP_201_CREATED)
def request_return(
    data: ReturnRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a return request for eligible delivered items."""
    return ReturnService.create_return_request(
        db=db,
        user_id=current_user.id,
        order_id=data.order_id,
        order_item_id=data.order_item_id,
        quantity=data.quantity,
        reason=data.reason
    )


@router.get("/order/{order_id}", response_model=List[ReturnRead])
def get_order_returns(order_id: int, db: Session = Depends(get_db)):
    """Retrieve return requests submitted for a given order."""
    return db.query(Return).filter(Return.order_id == order_id).all()


@router.post("/{return_id}/decision", response_model=ReturnRead)
def process_return_decision(
    return_id: int,
    approve: bool = Query(..., description="Approve or reject the return request"),
    notes: Optional[str] = Query(None, description="Resolution notes"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Approve or reject a customer return request (triggers simulated refund upon approval)."""
    return ReturnService.process_return_decision(db, return_id, approve=approve, notes=notes)
