"""
Shipping, Carrier Simulation, and Real-Time Tracking Service.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.models.order import Order, Shipment, ShipmentEvent
from app.websocket.manager import ws_manager


class ShippingService:
    @staticmethod
    def create_shipment(db: Session, order: Order, carrier: str = "Express Logistics") -> Shipment:
        tracking_num = f"TRK-{uuid.uuid4().hex[:10].upper()}"
        est_delivery = datetime.now(timezone.utc) + timedelta(days=3)

        shipment = Shipment(
            order_id=order.id,
            carrier_name=carrier,
            tracking_number=tracking_num,
            status="PREPARING",
            estimated_delivery=est_delivery,
            shipped_at=datetime.now(timezone.utc)
        )
        db.add(shipment)
        db.flush()

        initial_event = ShipmentEvent(
            shipment_id=shipment.id,
            status="PREPARING",
            location="Central Warehouse Bengaluru",
            description="Shipment package created and awaiting carrier pickup"
        )
        db.add(initial_event)
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def add_tracking_event(db: Session, shipment_id: int, status: str, location: str, description: str) -> ShipmentEvent:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise NotFoundException("Shipment", str(shipment_id))

        shipment.status = status
        if status == "DELIVERED":
            shipment.delivered_at = datetime.now(timezone.utc)
            # Update associated order status as well
            if shipment.order:
                shipment.order.status = "DELIVERED"

        event = ShipmentEvent(
            shipment_id=shipment.id,
            status=status,
            location=location,
            description=description,
            event_time=datetime.now(timezone.utc)
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Broadcast update to WebSocket topic
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(ws_manager.broadcast_to_topic(
                    f"order_{shipment.order_id}",
                    {"type": "SHIPMENT_UPDATE", "status": status, "location": location, "description": description}
                ))
        except Exception:
            pass

        return event

    @staticmethod
    def get_shipment_by_order_id(db: Session, order_id: int) -> Optional[Shipment]:
        return db.query(Shipment).filter(Shipment.order_id == order_id).first()

# Real-time carrier milestone progression generator
