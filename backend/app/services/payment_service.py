"""
Payment Simulation Service.
Clearly marked as a simulation engine. Provides realistic transaction lifecycle,
failure triggers, mock gateway receipts, and audit trails without handling real banking data.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.exceptions import PaymentFailedException, NotFoundException
from app.models.order import Order, Payment, PaymentStatus
from app.models.audit import AuditLog
from app.schemas.order import PaymentSimulationResponse


class PaymentService:
    @staticmethod
    def process_simulated_payment(
        db: Session,
        order: Order,
        payment_method: str = "CARD",
        simulate_failure: bool = False
    ) -> PaymentSimulationResponse:
        """Processes a simulated payment transaction for an order."""
        tx_id = f"SIM-TXN-{uuid.uuid4().hex[:12].upper()}"

        if simulate_failure:
            payment = Payment(
                order_id=order.id,
                user_id=order.customer_id,
                transaction_id=tx_id,
                payment_method=payment_method,
                status=PaymentStatus.FAILED.value,
                amount=order.total_amount,
                currency="INR",
                simulation_metadata={
                    "gateway": "Antigravity Mock Gateway",
                    "reason": "Simulated card decline / Insufficient test funds",
                    "simulated": True,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            db.add(payment)
            db.commit()

            # Record audit failure
            audit = AuditLog(
                user_id=order.customer_id,
                action="PAYMENT_FAILED_SIMULATION",
                resource_type="payment",
                resource_id=tx_id,
                status="FAILURE",
                details={"order_id": order.id, "amount": order.total_amount}
            )
            db.add(audit)
            db.commit()

            raise PaymentFailedException("Simulated payment failed as requested for testing", tx_id)

        # Successful payment simulation
        payment = Payment(
            order_id=order.id,
            user_id=order.customer_id,
            transaction_id=tx_id,
            payment_method=payment_method,
            status=PaymentStatus.SUCCESS.value,
            amount=order.total_amount,
            currency="INR",
            simulation_metadata={
                "gateway": "Antigravity Mock Gateway",
                "auth_code": f"AUTH-{uuid.uuid4().hex[:6].upper()}",
                "simulated": True,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "notice": "DEMONSTRATION SIMULATION ONLY - NO REAL MONEY WAS CHARGED"
            }
        )
        db.add(payment)

        # Audit log
        audit = AuditLog(
            user_id=order.customer_id,
            action="PAYMENT_SUCCESS_SIMULATION",
            resource_type="payment",
            resource_id=tx_id,
            status="SUCCESS",
            details={"order_id": order.id, "amount": order.total_amount, "method": payment_method}
        )
        db.add(audit)
        db.commit()

        return PaymentSimulationResponse(
            transaction_id=tx_id,
            status="SUCCESS",
            amount=order.total_amount,
            currency="INR",
            simulated=True,
            message="Payment successfully processed via Mock Payment Simulation Engine"
        )

    @staticmethod
    def simulate_refund(db: Session, order_id: int, refund_amount: float) -> Payment:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundException("Order", str(order_id))

        refund_tx_id = f"SIM-REFUND-{uuid.uuid4().hex[:12].upper()}"
        payment = Payment(
            order_id=order.id,
            user_id=order.customer_id,
            transaction_id=refund_tx_id,
            payment_method="REFUND",
            status=PaymentStatus.REFUNDED.value,
            amount=refund_amount,
            currency="INR",
            simulation_metadata={
                "gateway": "Antigravity Mock Gateway",
                "refund_for_order": order.order_number,
                "simulated": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
