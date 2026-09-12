"""
Customer Support Ticketing Service.
Manages customer inquiries, staff replies, and resolution lifecycles.
"""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.models.support import SupportTicket, SupportMessage
from app.schemas.support import SupportTicketCreate, SupportMessageCreate


class SupportService:
    @staticmethod
    def create_ticket(db: Session, user_id: int, data: SupportTicketCreate) -> SupportTicket:
        tck_num = f"TCK-{uuid.uuid4().hex[:8].upper()}"
        ticket = SupportTicket(
            ticket_number=tck_num,
            user_id=user_id,
            subject=data.subject,
            category=data.category,
            priority=data.priority,
            status="OPEN"
        )
        db.add(ticket)
        db.flush()

        initial_msg = SupportMessage(
            ticket_id=ticket.id,
            sender_id=user_id,
            message=data.initial_message,
            is_staff_reply=False
        )
        db.add(initial_msg)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def add_message(db: Session, ticket_id: int, sender_id: int, message: str, is_staff: bool = False) -> SupportMessage:
        ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
        if not ticket:
            raise NotFoundException("SupportTicket", str(ticket_id))

        msg = SupportMessage(
            ticket_id=ticket.id,
            sender_id=sender_id,
            message=message,
            is_staff_reply=is_staff
        )
        db.add(msg)

        if is_staff and ticket.status == "OPEN":
            ticket.status = "IN_PROGRESS"

        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_ticket(db: Session, ticket_id: int, user_id: Optional[int] = None, is_staff: bool = False) -> SupportTicket:
        query = db.query(SupportTicket).filter(SupportTicket.id == ticket_id)
        if not is_staff and user_id:
            query = query.filter(SupportTicket.user_id == user_id)
        ticket = query.first()
        if not ticket:
            raise NotFoundException("SupportTicket", str(ticket_id))
        return ticket

    @staticmethod
    def list_user_tickets(db: Session, user_id: int) -> List[SupportTicket]:
        return db.query(SupportTicket).filter(SupportTicket.user_id == user_id).order_by(SupportTicket.created_at.desc()).all()

    @staticmethod
    def list_all_tickets(db: Session, status: Optional[str] = None) -> List[SupportTicket]:
        q = db.query(SupportTicket)
        if status:
            q = q.filter(SupportTicket.status == status)
        return q.order_by(SupportTicket.created_at.desc()).all()
