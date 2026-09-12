"""
Customer Support Tickets and Messages Models.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class SupportTicket(Base, TimestampMixin):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    category = Column(String(50), default="ORDER", nullable=False)  # ORDER, PRODUCT, PAYMENT, RETURN, ACCOUNT, OTHER
    priority = Column(String(30), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    status = Column(String(30), default="OPEN", nullable=False, index=True)  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    assigned_agent_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="support_tickets")
    assigned_agent = relationship("User", foreign_keys=[assigned_agent_id])
    messages = relationship("SupportMessage", back_populates="ticket", cascade="all, delete-orphan")


class SupportMessage(Base, TimestampMixin):
    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    is_staff_reply = Column(Boolean, default=False, nullable=False)
    attachments = Column(JSON, default=list, nullable=False)

    ticket = relationship("SupportTicket", back_populates="messages")
    sender = relationship("User")
