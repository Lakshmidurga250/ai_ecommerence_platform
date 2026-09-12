"""
Support Ticket and Support Message Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SupportMessageCreate(BaseModel):
    message: str


class SupportMessageRead(BaseModel):
    id: int
    ticket_id: int
    sender_id: int
    message: str
    is_staff_reply: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupportTicketCreate(BaseModel):
    subject: str
    category: str = "ORDER"  # ORDER, PRODUCT, PAYMENT, RETURN, ACCOUNT, OTHER
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, URGENT
    initial_message: str


class SupportTicketStatusUpdate(BaseModel):
    status: str  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    assigned_agent_id: Optional[int] = None


class SupportTicketRead(BaseModel):
    id: int
    ticket_number: str
    user_id: int
    subject: str
    category: str
    priority: str
    status: str
    assigned_agent_id: Optional[int] = None
    messages: List[SupportMessageRead] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
