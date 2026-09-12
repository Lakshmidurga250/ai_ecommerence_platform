"""
Business Analytics & Operational Metrics Engine.
Queries genuine database transactions to calculate platform and seller KPIs.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.order import Order, OrderItem
from app.models.product import Product, Category
from app.models.user import User
from app.models.seller import Seller
from app.models.inventory import Inventory
from app.models.analytics import BehaviorEvent, FraudAlert
from app.schemas.analytics import BusinessOverviewMetrics, SellerDashboardMetrics


class AnalyticsService:
    @staticmethod
    def record_behavior_event(
        db: Session,
        event_type: str,
        user_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BehaviorEvent:
        event = BehaviorEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            product_id=product_id,
            category_id=category_id,
            event_metadata=metadata or {}
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Update recommender engine memory if user_id and product_id are present
        if user_id and product_id:
            from ai.recommendations.recommender import recommender_engine
            recommender_engine.record_interaction(user_id, product_id, event_type)

        return event

    @staticmethod
    def get_business_overview(db: Session) -> BusinessOverviewMetrics:
        """Calculates platform-level financial and inventory metrics from raw DB tables."""
        # Revenue and orders
        order_stats = db.query(
            func.sum(Order.total_amount).label("total_rev"),
            func.count(Order.id).label("total_orders"),
            func.avg(Order.total_amount).label("aov")
        ).filter(Order.status.in_(["CONFIRMED", "PROCESSING", "PACKED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED"])).first()

        total_rev = round(float(order_stats.total_rev or 0.0), 2)
        total_orders = int(order_stats.total_orders or 0)
        aov = round(float(order_stats.aov or 0.0), 2)

        total_customers = db.query(User).count()
        total_sellers = db.query(Seller).count()
        total_products = db.query(Product).count()

        pending_orders = db.query(Order).filter(Order.status.in_(["PENDING", "CONFIRMED", "PROCESSING"])).count()

        # Low stock items
        low_stock_count = db.query(Inventory).filter(
            (Inventory.quantity - Inventory.reserved_quantity) <= Inventory.reorder_level
        ).count()

        fraud_alerts = db.query(FraudAlert).filter(FraudAlert.status == "PENDING_REVIEW").count()

        # Revenue Trend (Last 7 days)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        daily_trend_rows = db.query(
            func.date(Order.created_at).label("day"),
            func.sum(Order.total_amount).label("rev"),
            func.count(Order.id).label("orders")
        ).filter(Order.created_at >= seven_days_ago, Order.status != "CANCELLED").group_by(func.date(Order.created_at)).all()

        revenue_chart = [
            {"date": str(r.day), "revenue": round(float(r.rev or 0), 2), "orders": int(r.orders or 0)}
            for r in daily_trend_rows
        ]

        # Top selling products
        top_prods_query = db.query(
            Product.id, Product.name, Product.sales_count, Product.price
        ).order_by(desc(Product.sales_count)).limit(5).all()

        top_products = [
            {"id": p.id, "name": p.name, "sales": p.sales_count, "price": p.price}
            for p in top_prods_query
        ]

        # Category distribution
        cat_dist = db.query(
            Category.name, func.count(Product.id).label("count")
        ).join(Product, Product.category_id == Category.id).group_by(Category.name).all()

        category_distribution = [{"category": c.name, "count": int(c.count)} for c in cat_dist]

        return BusinessOverviewMetrics(
            total_revenue=total_rev,
            total_orders=total_orders,
            total_customers=total_customers,
            total_sellers=total_sellers,
            total_products=total_products,
            average_order_value=aov,
            pending_orders_count=pending_orders,
            low_stock_items_count=low_stock_count,
            fraud_alerts_count=fraud_alerts,
            revenue_chart_data=revenue_chart,
            top_selling_products=top_products,
            category_distribution=category_distribution
        )

    @staticmethod
    def get_seller_metrics(db: Session, seller_id: int) -> SellerDashboardMetrics:
        """Calculates seller-isolated KPIs."""
        seller = db.query(Seller).filter(Seller.id == seller_id).first()
        store_name = seller.store_name if seller else f"Seller #{seller_id}"

        # Sales and revenue for this seller
        stats = db.query(
            func.sum(OrderItem.total).label("revenue"),
            func.count(func.distinct(OrderItem.order_id)).label("order_count"),
            func.avg(OrderItem.total).label("aov")
        ).filter(OrderItem.seller_id == seller_id).first()

        total_rev = round(float(stats.revenue or 0.0), 2)
        total_orders = int(stats.order_count or 0)
        aov = round(float(stats.aov or 0.0), 2)

        total_prods = db.query(Product).filter(Product.seller_id == seller_id).count()

        # Seller low stock
        low_stock_count = db.query(Inventory).join(Product).filter(
            Product.seller_id == seller_id,
            (Inventory.quantity - Inventory.reserved_quantity) <= Inventory.reorder_level
        ).count()

        # Top products for this seller
        top_prods = db.query(Product.id, Product.name, Product.sales_count, Product.price).filter(
            Product.seller_id == seller_id
        ).order_by(desc(Product.sales_count)).limit(5).all()

        return SellerDashboardMetrics(
            seller_id=seller_id,
            store_name=store_name,
            total_revenue=total_rev,
            total_orders=total_orders,
            total_products=total_prods,
            average_order_value=aov,
            low_stock_count=low_stock_count,
            top_products=[{"id": p.id, "name": p.name, "sales": p.sales_count, "price": p.price} for p in top_prods]
        )
