"""
Payment Simulation API Endpoints.
Clearly marked as mock simulation for educational/testing purposes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.order import Order
from app.schemas.order import PaymentSimulateRequest, PaymentSimulationResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payment Simulation"])


@router.post("/simulate", response_model=PaymentSimulationResponse)
def simulate_payment(
    data: PaymentSimulateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute simulated payment gateway transaction with transparent mock transaction IDs."""
    order = db.query(Order).filter(Order.id == data.order_id, Order.customer_id == current_user.id).first()
    if not order:
        raise NotFoundException("Order", str(data.order_id))

    return PaymentService.process_simulated_payment(
        db=db,
        order=order,
        payment_method=data.payment_method,
        simulate_failure=data.simulate_failure
    )
