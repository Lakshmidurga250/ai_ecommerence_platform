"""
Returns and Refund Management Service.
Validates return eligibility, manages return states, and triggers simulated refunds.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AppException
from app.models.order import Order, OrderItem, Return, ReturnItem
from app.services.payment_service import PaymentService


class ReturnService:
    @staticmethod
    def create_return_request(db: Session, user_id: int, order_id: int, order_item_id: int, quantity: int, reason: str) -> Return:
        order = db.query(Order).filter(Order.id == order_id, Order.customer_id == user_id).first()
        if not order:
            raise NotFoundException("Order", str(order_id))

        if order.status not in ("DELIVERED", "SHIPPED"):
            raise AppException("Orders can only be returned after delivery has been initiated or completed", 400, "RETURN_NOT_ELIGIBLE")

        order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id, OrderItem.order_id == order_id).first()
        if not order_item:
            raise NotFoundException("OrderItem", str(order_item_id))

        if quantity > order_item.quantity:
            raise AppException("Return quantity cannot exceed purchased quantity", 400, "INVALID_RETURN_QUANTITY")

        refund_calc = round((order_item.total / order_item.quantity) * quantity, 2)

        return_record = Return(
            order_id=order.id,
            user_id=user_id,
            status="REQUESTED",
            reason=reason,
            refund_amount=refund_calc
        )
        db.add(return_record)
        db.flush()

        item = ReturnItem(
            return_id=return_record.id,
            order_item_id=order_item.id,
            quantity=quantity,
            reason=reason
        )
        db.add(item)
        order.status = "RETURN_REQUESTED"

        db.commit()
        db.refresh(return_record)
        return return_record

    @staticmethod
    def process_return_decision(db: Session, return_id: int, approve: bool, notes: Optional[str] = None) -> Return:
        return_rec = db.query(Return).filter(Return.id == return_id).first()
        if not return_rec:
            raise NotFoundException("Return", str(return_id))

        if approve:
            return_rec.status = "APPROVED"
            return_rec.resolution_notes = notes or "Return approved. Initiating refund simulation."
            # Trigger simulated refund
            PaymentService.simulate_refund(db, return_rec.order_id, return_rec.refund_amount)
            return_rec.status = "REFUNDED"
            return_rec.order.status = "REFUNDED"
        else:
            return_rec.status = "REJECTED"
            return_rec.resolution_notes = notes or "Return request rejected according to platform policy."

        db.commit()
        db.refresh(return_rec)
        return return_rec
