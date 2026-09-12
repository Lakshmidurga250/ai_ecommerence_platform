"""
Customer Support Ticketing API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.support import SupportTicketCreate, SupportTicketRead, SupportMessageCreate, SupportMessageRead
from app.services.support_service import SupportService

router = APIRouter(prefix="/support", tags=["Customer Support"])


@router.post("/tickets", response_model=SupportTicketRead, status_code=status.HTTP_201_CREATED)
def open_support_ticket(
    data: SupportTicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Open a new support inquiry ticket."""
    return SupportService.create_ticket(db, current_user.id, data)


@router.get("/tickets", response_model=List[SupportTicketRead])
def list_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List customer's support tickets and active threads."""
    is_staff = any(r in current_user.role_names for r in ["ADMIN", "SUPPORT"])
    if is_staff:
        return SupportService.list_all_tickets(db)
    return SupportService.list_user_tickets(db, current_user.id)


@router.get("/tickets/{ticket_id}", response_model=SupportTicketRead)
def get_ticket_details(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get support ticket conversation history."""
    is_staff = any(r in current_user.role_names for r in ["ADMIN", "SUPPORT"])
    return SupportService.get_ticket(db, ticket_id, user_id=current_user.id, is_staff=is_staff)


@router.post("/tickets/{ticket_id}/messages", response_model=SupportMessageRead, status_code=status.HTTP_201_CREATED)
def reply_to_ticket(
    ticket_id: int,
    data: SupportMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reply to an existing support ticket thread."""
    is_staff = any(r in current_user.role_names for r in ["ADMIN", "SUPPORT"])
    return SupportService.add_message(db, ticket_id, current_user.id, data.message, is_staff=is_staff)
