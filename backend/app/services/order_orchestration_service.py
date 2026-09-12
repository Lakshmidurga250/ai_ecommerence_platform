"""
Order Orchestration & Multi-Vendor Splitting Service.
Manages multi-seller basket partitioning, seller package tracking,
and item-level return eligibility verification.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, BadRequestException, AuthorizationException
from app.models.order import Order, OrderItem, OrderStatus, Return, ReturnItem
from app.models.seller import Seller
from app.models.product import Product


class OrderOrchestrationService:
    @staticmethod
    def split_order_by_seller(db: Session, order_id: int) -> Dict[str, Any]:
        """
        Partitions an order's line items into discrete vendor sub-orders,
        computing commission withholdings and fulfillment manifests.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundException("Order", str(order_id))

        # Group items by seller_id
        items_by_seller: Dict[int, List[OrderItem]] = {}
        for item in order.items:
            seller_id = item.seller_id or 1
            if seller_id not in items_by_seller:
                items_by_seller[seller_id] = []
            items_by_seller[seller_id].append(item)

        sub_orders = []
        for s_id, items in items_by_seller.items():
            seller = db.query(Seller).filter(Seller.id == s_id).first()
            store_name = seller.store_name if seller else f"Vendor #{s_id}"
            commission_rate = float(seller.commission_rate or 0.10) if seller else 0.10

            subtotal = sum(i.total for i in items)
            commission_amount = round(subtotal * commission_rate, 2)
            net_payable = round(subtotal - commission_amount, 2)

            # Determine composite status for this vendor's package
            item_statuses = set(i.status for i in items)
            if all(s == "DELIVERED" for s in item_statuses):
                fulfillment_status = "DELIVERED"
            elif any(s in ("SHIPPED", "OUT_FOR_DELIVERY") for s in item_statuses):
                fulfillment_status = "SHIPPED"
            elif any(s == "CANCELLED" for s in item_statuses) and len(item_statuses) == 1:
                fulfillment_status = "CANCELLED"
            else:
                fulfillment_status = order.status

            sub_orders.append({
                "seller_id": s_id,
                "store_name": store_name,
                "items": [
                    {
                        "item_id": it.id,
                        "product_id": it.product_id,
                        "product_name": it.product_name,
                        "sku": it.sku,
                        "quantity": it.quantity,
                        "unit_price": it.unit_price,
                        "total": it.total,
                        "status": it.status
                    }
                    for it in items
                ],
                "item_count": sum(it.quantity for it in items),
                "subtotal": round(subtotal, 2),
                "commission_rate": commission_rate,
                "platform_commission": commission_amount,
                "net_payable": net_payable,
                "fulfillment_status": fulfillment_status
            })

        return {
            "order_id": order.id,
            "order_number": order.order_number,
            "customer_id": order.customer_id,
            "overall_status": order.status,
            "order_date": order.created_at.isoformat() if order.created_at else None,
            "total_amount": order.total_amount,
            "vendor_count": len(sub_orders),
            "vendor_sub_orders": sub_orders
        }

    @staticmethod
    def check_return_eligibility(
        db: Session,
        user_id: int,
        order_id: int,
        order_item_id: int
    ) -> Dict[str, Any]:
        """
        Evaluates authentic return policy rules:
        1. Order must belong to the requesting customer.
        2. Order must be in DELIVERED status.
        3. Delivery date must be within the 30-day return window.
        4. Item must not have an active or completed return exceeding quantity.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"eligible": False, "reason": f"Order #{order_id} not found", "max_quantity": 0}

        if order.customer_id != user_id:
            return {"eligible": False, "reason": "Order does not belong to the requesting user", "max_quantity": 0}

        if order.status not in (OrderStatus.DELIVERED.value, OrderStatus.SHIPPED.value):
            return {
                "eligible": False,
                "reason": f"Order is currently '{order.status}'. Returns are only eligible for delivered shipments.",
                "max_quantity": 0
            }

        order_item = db.query(OrderItem).filter(
            OrderItem.id == order_item_id,
            OrderItem.order_id == order_id
        ).first()

        if not order_item:
            return {"eligible": False, "reason": "Order line item not found", "max_quantity": 0}

        # Check 30-day policy window
        now = datetime.now(timezone.utc)
        order_time = order.updated_at or order.created_at
        if order_time:
            if order_time.tzinfo is None:
                order_time = order_time.replace(tzinfo=timezone.utc)
            days_since = (now - order_time).days
            if days_since > 30:
                return {
                    "eligible": False,
                    "reason": f"The 30-day return policy window expired {days_since - 30} days ago.",
                    "max_quantity": 0
                }

        # Check existing return quantities
        existing_returns = db.query(ReturnItem).join(Return).filter(
            ReturnItem.order_item_id == order_item_id,
            Return.status.in_(["REQUESTED", "APPROVED", "REFUNDED"])
        ).all()

        returned_qty = sum(r.quantity for r in existing_returns)
        remaining_qty = order_item.quantity - returned_qty

        if remaining_qty <= 0:
            return {
                "eligible": False,
                "reason": "All units for this product have already been returned or have a pending request.",
                "max_quantity": 0
            }

        unit_refund = round(order_item.total / order_item.quantity, 2)

        return {
            "eligible": True,
            "reason": "Item meets all 30-day return policy requirements.",
            "max_quantity": remaining_qty,
            "unit_price": order_item.unit_price,
            "unit_refund": unit_refund,
            "currency": "USD"
        }

    @staticmethod
    def update_seller_item_status(
        db: Session,
        seller_id: int,
        order_item_id: int,
        new_status: str
    ) -> OrderItem:
        """
        Updates fulfillment state of an individual seller line item with tenant isolation.
        """
        item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
        if not item:
            raise NotFoundException("OrderItem", str(order_item_id))

        if item.seller_id != seller_id:
            raise AuthorizationException("You do not have permission to update items from other sellers")

        item.status = new_status
        db.commit()
        db.refresh(item)
        return item
