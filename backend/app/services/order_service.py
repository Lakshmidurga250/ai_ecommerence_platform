"""
Order Management & Complete Order Lifecycle Service.
Coordinates checkout, stock reservation, fraud risk evaluation, payment simulation, and state transitions.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, AppException, InsufficientStockException, AuthorizationException
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.cart import Cart, CartItem, Coupon, CouponUsage
from app.models.product import Product
from app.models.user import Address
from app.models.analytics import BehaviorEvent
from app.schemas.order import CheckoutRequest
from app.services.cart_service import CartService
from app.services.inventory_service import InventoryService
from app.services.payment_service import PaymentService
from app.services.shipping_service import ShippingService
from app.websocket.manager import ws_manager


class OrderService:
    @staticmethod
    def checkout(db: Session, user_id: int, data: CheckoutRequest) -> Order:
        """Executes full checkout transaction: stock reservation, order creation, payment simulation, and shipment."""
        # 1. Validate shipping address
        address = db.query(Address).filter(Address.id == data.shipping_address_id, Address.user_id == user_id).first()
        if not address:
            raise NotFoundException("Shipping address", str(data.shipping_address_id))

        # 2. Get and recalculate cart
        cart_calc = CartService.calculate_cart(db, user_id, coupon_code=data.coupon_code)
        items: List[CartItem] = cart_calc["items"]
        if not items:
            raise AppException("Cannot checkout with an empty shopping cart", 400, "EMPTY_CART")

        order_number = f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # 3. Reserve stock for all items
        reserved_items = []
        try:
            for item in items:
                InventoryService.reserve_stock(db, item.product_id, item.quantity, reference_id=order_number)
                reserved_items.append((item.product_id, item.quantity))
        except InsufficientStockException as e:
            # Rollback previously reserved items in this loop
            for prod_id, qty in reserved_items:
                InventoryService.release_stock(db, prod_id, qty, reference_id=order_number)
            raise e

        # 4. Create Order Record
        order = Order(
            order_number=order_number,
            customer_id=user_id,
            shipping_address_id=data.shipping_address_id,
            status=OrderStatus.CONFIRMED.value,
            subtotal=cart_calc["subtotal"],
            discount_amount=cart_calc["discount_amount"],
            tax_amount=cart_calc["tax_amount"],
            shipping_fee=cart_calc["shipping_fee"],
            total_amount=cart_calc["total_amount"],
            coupon_code=data.coupon_code,
            notes=data.customer_notes
        )
        db.add(order)
        db.flush()

        # 5. Create Order Items
        for item in items:
            p = item.product
            unit_price = item.variant.price if item.variant else p.price
            item_sub = unit_price * item.quantity
            item_tax = item_sub * (p.tax_rate or 0.18)
            order_item = OrderItem(
                order_id=order.id,
                product_id=p.id,
                variant_id=item.variant_id,
                seller_id=p.seller_id,
                product_name=p.name,
                sku=p.sku,
                unit_price=unit_price,
                quantity=item.quantity,
                subtotal=round(item_sub, 2),
                tax_amount=round(item_tax, 2),
                total=round(item_sub + item_tax, 2),
                status="CONFIRMED"
            )
            db.add(order_item)
            # Increment product sales count
            p.sales_count += item.quantity

        # 6. Apply coupon usage if applicable
        if data.coupon_code and cart_calc["discount_amount"] > 0:
            coupon = db.query(Coupon).filter(Coupon.code == data.coupon_code.strip().upper()).first()
            if coupon:
                coupon.usage_count += 1
                usage = CouponUsage(
                    coupon_id=coupon.id,
                    user_id=user_id,
                    order_id=order.id,
                    discount_amount=cart_calc["discount_amount"]
                )
                db.add(usage)

        # 7. Execute Simulated Payment
        PaymentService.process_simulated_payment(db, order, payment_method=data.payment_method)

        # 8. Create Carrier Shipment
        ShippingService.create_shipment(db, order)

        # 9. Extract event data before clearing cart
        item_events_data = [(item.product_id, item.quantity) for item in items]
        CartService.clear_cart(db, user_id)

        # 10. Record Behavioral Event for AI Pipeline
        for prod_id, qty in item_events_data:
            event = BehaviorEvent(
                user_id=user_id,
                event_type="PURCHASE",
                product_id=prod_id,
                event_metadata={"order_id": order.id, "amount": order.total_amount, "qty": qty}
            )
            db.add(event)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_order_status(db: Session, order_id: int, new_status: str, seller_id: Optional[int] = None, is_admin: bool = False) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundException("Order", str(order_id))

        if seller_id and not is_admin:
            # Verify seller has items in this order
            has_items = any(item.seller_id == seller_id for item in order.items)
            if not has_items:
                raise AuthorizationException("Cannot modify orders outside your seller account")

        old_status = order.status
        order.status = new_status

        # Stock state transitions
        if new_status == OrderStatus.SHIPPED.value and old_status != OrderStatus.SHIPPED.value:
            for item in order.items:
                InventoryService.deduct_reserved_stock(db, item.product_id, item.quantity, order.order_number)
            if order.shipment:
                order.shipment.status = "IN_TRANSIT"

        elif new_status == OrderStatus.CANCELLED.value and old_status not in (OrderStatus.CANCELLED.value, OrderStatus.DELIVERED.value):
            for item in order.items:
                InventoryService.release_stock(db, item.product_id, item.quantity, order.order_number)

        db.commit()
        db.refresh(order)

        # Broadcast real-time WebSocket update
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(ws_manager.broadcast_to_topic(
                    f"order_{order.id}",
                    {"type": "ORDER_STATUS_UPDATE", "order_id": order.id, "status": new_status, "order_number": order.order_number}
                ))
        except Exception:
            pass

        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user_id: Optional[int] = None, seller_id: Optional[int] = None, is_admin: bool = False) -> Order:
        query = db.query(Order).filter(Order.id == order_id)
        if user_id and not is_admin:
            query = query.filter(Order.customer_id == user_id)
        order = query.first()
        if not order:
            raise NotFoundException("Order", str(order_id))
        return order

    @staticmethod
    def list_customer_orders(db: Session, user_id: int) -> List[Order]:
        return db.query(Order).filter(Order.customer_id == user_id).order_by(Order.created_at.desc()).all()

    @staticmethod
    def list_seller_orders(db: Session, seller_id: int) -> List[Order]:
        # Orders that contain items sold by this seller
        return db.query(Order).join(OrderItem).filter(OrderItem.seller_id == seller_id).distinct().order_by(Order.created_at.desc()).all()

    @staticmethod
    def list_all_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
