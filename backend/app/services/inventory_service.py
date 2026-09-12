"""
Inventory and Multi-Warehouse Intelligence Service.
Calculates Available Stock = Total Quantity - Reserved Quantity.
Handles stock reservations, stock movements, and automated low-stock alerts.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.exceptions import NotFoundException, InsufficientStockException
from app.models.inventory import Warehouse, Inventory, InventoryMovement
from app.models.product import Product
from app.schemas.inventory import LowStockAlert


class InventoryService:
    @staticmethod
    def get_or_create_inventory(db: Session, warehouse_id: int, product_id: int) -> Inventory:
        inv = db.query(Inventory).filter(
            Inventory.warehouse_id == warehouse_id,
            Inventory.product_id == product_id
        ).first()
        if not inv:
            inv = Inventory(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=0,
                reserved_quantity=0,
                reorder_level=10
            )
            db.add(inv)
            db.flush()
        return inv

    @staticmethod
    def reserve_stock(db: Session, product_id: int, quantity: int, reference_id: str) -> bool:
        """Reserve available stock for a pending order."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundException("Product", str(product_id))

        # Find inventory across warehouses
        inventories = db.query(Inventory).filter(Inventory.product_id == product_id).all()
        total_available = sum(inv.available_quantity for inv in inventories)

        if total_available < quantity:
            raise InsufficientStockException(product.name, quantity, total_available)

        remaining_to_reserve = quantity
        for inv in inventories:
            avail = inv.available_quantity
            if avail <= 0:
                continue
            reserve_from_this = min(avail, remaining_to_reserve)
            inv.reserved_quantity += reserve_from_this
            remaining_to_reserve -= reserve_from_this

            movement = InventoryMovement(
                inventory_id=inv.id,
                movement_type="RESERVATION",
                quantity=reserve_from_this,
                reference_type="ORDER_RESERVATION",
                reference_id=reference_id,
                notes=f"Reserved for order {reference_id}"
            )
            db.add(movement)

            if remaining_to_reserve == 0:
                break

        # Also update product catalog denormalized stock
        product.stock = max(0, product.stock - quantity)
        db.commit()
        return True

    @staticmethod
    def release_stock(db: Session, product_id: int, quantity: int, reference_id: str):
        """Release reserved stock back to available when an order is cancelled."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return

        inventories = db.query(Inventory).filter(Inventory.product_id == product_id).all()
        remaining_to_release = quantity
        for inv in inventories:
            if inv.reserved_quantity <= 0:
                continue
            release_from_this = min(inv.reserved_quantity, remaining_to_release)
            inv.reserved_quantity -= release_from_this
            remaining_to_release -= release_from_this

            movement = InventoryMovement(
                inventory_id=inv.id,
                movement_type="RELEASE",
                quantity=release_from_this,
                reference_type="ORDER_CANCELLATION",
                reference_id=reference_id,
                notes=f"Released reservation from order {reference_id}"
            )
            db.add(movement)

            if remaining_to_release == 0:
                break

        product.stock += quantity
        db.commit()

    @staticmethod
    def deduct_reserved_stock(db: Session, product_id: int, quantity: int, reference_id: str):
        """Deduct reserved stock permanently upon physical shipment dispatch."""
        inventories = db.query(Inventory).filter(Inventory.product_id == product_id).all()
        remaining = quantity
        for inv in inventories:
            if inv.reserved_quantity <= 0:
                continue
            deduct_from_this = min(inv.reserved_quantity, remaining)
            inv.quantity -= deduct_from_this
            inv.reserved_quantity -= deduct_from_this
            remaining -= deduct_from_this

            movement = InventoryMovement(
                inventory_id=inv.id,
                movement_type="OUTBOUND",
                quantity=deduct_from_this,
                reference_type="SHIPMENT_DISPATCH",
                reference_id=reference_id,
                notes=f"Dispatched order {reference_id}"
            )
            db.add(movement)

            if remaining == 0:
                break
        db.commit()

    @staticmethod
    def adjust_stock(db: Session, warehouse_id: int, product_id: int, quantity_change: int, reason: str, reference_id: Optional[str] = None) -> Inventory:
        inv = InventoryService.get_or_create_inventory(db, warehouse_id, product_id)
        product = db.query(Product).filter(Product.id == product_id).first()

        inv.quantity = max(0, inv.quantity + quantity_change)
        if product:
            product.stock = max(0, product.stock + quantity_change)

        movement = InventoryMovement(
            inventory_id=inv.id,
            movement_type="INBOUND" if quantity_change > 0 else "ADJUSTMENT",
            quantity=abs(quantity_change),
            reference_type="MANUAL_ADJUSTMENT",
            reference_id=reference_id,
            notes=reason
        )
        db.add(movement)
        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def get_low_stock_alerts(db: Session, seller_id: Optional[int] = None) -> List[LowStockAlert]:
        """Generate low-stock intelligence alerts based on available units <= reorder level."""
        query = db.query(Product).filter(Product.is_active == True)
        if seller_id:
            query = query.filter(Product.seller_id == seller_id)

        products = query.all()
        alerts = []
        for p in products:
            inv_items = db.query(Inventory).filter(Inventory.product_id == p.id).all()
            total_qty = sum(i.quantity for i in inv_items)
            total_reserved = sum(i.reserved_quantity for i in inv_items)
            available = max(0, total_qty - total_reserved)
            reorder = min((i.reorder_level for i in inv_items), default=10)

            if available <= reorder:
                urgency = "CRITICAL" if available == 0 else ("HIGH" if available <= reorder // 2 else "MEDIUM")
                alerts.append(LowStockAlert(
                    product_id=p.id,
                    product_name=p.name,
                    sku=p.sku,
                    current_stock=total_qty,
                    reserved_stock=total_reserved,
                    available_stock=available,
                    reorder_level=reorder,
                    urgency=urgency
                ))
        return alerts
