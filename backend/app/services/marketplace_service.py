"""
Multi-Vendor Marketplace Service.
Orchestrates seller performance metrics, financial scorecards, commission reconciliation,
and seller payout settlements.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import NotFoundException, BadRequestException, ConflictException
from app.models.seller import Seller, SellerProfile, SellerStatus
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus, Return
from app.models.review import Review
from app.models.catalog_expansion import SellerPayout


class MarketplaceService:
    @staticmethod
    def get_seller_scorecard(db: Session, seller_id: int) -> Dict[str, Any]:
        """
        Computes dynamic performance scorecard, ratings, fulfillment rates,
        and financial reconciliations for a vendor.
        """
        seller = db.query(Seller).filter(Seller.id == seller_id).first()
        if not seller:
            raise NotFoundException("Seller", str(seller_id))

        # Products count
        product_ids = [p.id for p in db.query(Product.id).filter(Product.seller_id == seller_id).all()]
        total_products = len(product_ids)

        # Order Items for this seller
        seller_items = db.query(OrderItem).filter(OrderItem.seller_id == seller_id).all()
        total_units_sold = sum(item.quantity for item in seller_items)
        gross_sales = sum(item.total for item in seller_items)

        # Fulfillment breakdown based on parent order or item status
        unique_order_ids = list(set(item.order_id for item in seller_items))
        total_orders_count = len(unique_order_ids)

        orders = db.query(Order).filter(Order.id.in_(unique_order_ids)).all() if unique_order_ids else []
        delivered_count = sum(1 for o in orders if o.status == OrderStatus.DELIVERED.value)
        shipped_count = sum(1 for o in orders if o.status in (OrderStatus.SHIPPED.value, OrderStatus.OUT_FOR_DELIVERY.value))
        cancelled_count = sum(1 for o in orders if o.status == OrderStatus.CANCELLED.value)
        returned_count = sum(1 for o in orders if o.status in (OrderStatus.RETURNED.value, OrderStatus.RETURN_REQUESTED.value))

        fulfilled_count = delivered_count + shipped_count
        fulfillment_rate = round((fulfilled_count / max(1, total_orders_count - cancelled_count)) * 100, 1) if (total_orders_count - cancelled_count) > 0 else 100.0
        return_rate = round((returned_count / max(1, fulfilled_count)) * 100, 1) if fulfilled_count > 0 else 0.0
        cancellation_rate = round((cancelled_count / max(1, total_orders_count)) * 100, 1) if total_orders_count > 0 else 0.0

        # Review & Rating aggregation
        reviews = db.query(Review).filter(Review.product_id.in_(product_ids)).all() if product_ids else []
        avg_rating = round(sum(r.rating for r in reviews) / max(1, len(reviews)), 2) if reviews else float(seller.rating or 5.0)

        # Financial reconciliation
        commission_rate = float(seller.commission_rate or 0.10)
        total_commission_deducted = round(gross_sales * commission_rate, 2)
        net_seller_earnings = round(gross_sales - total_commission_deducted, 2)

        # Historical payouts
        payouts = db.query(SellerPayout).filter(SellerPayout.seller_id == seller_id).all()
        processed_payouts = sum(p.net_amount for p in payouts if p.status == "PROCESSED")
        pending_payouts = sum(p.net_amount for p in payouts if p.status == "PENDING")
        available_balance = max(0.0, round(net_seller_earnings - processed_payouts - pending_payouts, 2))

        # Update seller cached stats
        seller.total_sales_count = total_units_sold
        seller.rating = avg_rating
        db.commit()

        return {
            "seller_id": seller.id,
            "store_name": seller.store_name,
            "status": seller.status,
            "commission_rate": commission_rate,
            "catalog_metrics": {
                "total_products": total_products,
                "total_reviews": len(reviews),
                "average_rating": avg_rating
            },
            "fulfillment_metrics": {
                "total_orders": total_orders_count,
                "total_units_sold": total_units_sold,
                "fulfilled_orders": fulfilled_count,
                "cancelled_orders": cancelled_count,
                "returned_orders": returned_count,
                "fulfillment_rate_pct": min(100.0, fulfillment_rate),
                "return_rate_pct": min(100.0, return_rate),
                "cancellation_rate_pct": min(100.0, cancellation_rate)
            },
            "financial_metrics": {
                "gross_sales": round(gross_sales, 2),
                "platform_commission": total_commission_deducted,
                "net_earnings": net_seller_earnings,
                "total_paid_out": round(processed_payouts, 2),
                "pending_payouts": round(pending_payouts, 2),
                "available_balance": available_balance
            }
        }

    @staticmethod
    def request_payout(
        db: Session,
        seller_id: int,
        amount: float,
        notes: Optional[str] = None
    ) -> SellerPayout:
        """
        Submits a payout withdrawal request against the vendor's available balance.
        """
        scorecard = MarketplaceService.get_seller_scorecard(db, seller_id)
        available = scorecard["financial_metrics"]["available_balance"]

        if amount <= 0:
            raise BadRequestException("Payout request amount must be greater than zero")

        if amount > available:
            raise BadRequestException(
                f"Requested amount (${amount:.2f}) exceeds available balance (${available:.2f})"
            )

        now = datetime.now(timezone.utc)
        payout_ref = f"PAY-{uuid.uuid4().hex[:10].upper()}"

        commission_est = round(amount * scorecard["commission_rate"], 2)
        payout = SellerPayout(
            seller_id=seller_id,
            amount=amount,
            commission_deducted=commission_est,
            net_amount=amount,
            status="PENDING",
            payout_reference=payout_ref,
            period_start=now - timedelta(days=30),
            period_end=now
        )
        db.add(payout)
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def list_seller_payouts(db: Session, seller_id: int) -> List[SellerPayout]:
        """Returns disbursement records for a seller."""
        return (
            db.query(SellerPayout)
            .filter(SellerPayout.seller_id == seller_id)
            .order_by(SellerPayout.created_at.desc())
            .all()
        )

    @staticmethod
    def process_payout_disbursement(
        db: Session,
        payout_id: int,
        action: str,  # "APPROVE", "REJECT", "COMPLETE"
        reference: Optional[str] = None
    ) -> SellerPayout:
        """
        Admin transition of seller payout record.
        """
        payout = db.query(SellerPayout).filter(SellerPayout.id == payout_id).first()
        if not payout:
            raise NotFoundException("SellerPayout", str(payout_id))

        if action == "APPROVE" or action == "COMPLETE":
            payout.status = "PROCESSED"
            if reference:
                payout.payout_reference = reference
        elif action == "REJECT":
            payout.status = "FAILED"
        else:
            raise BadRequestException(f"Invalid payout action: {action}")

        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def get_marketplace_overview(db: Session) -> Dict[str, Any]:
        """
        Admin platform-wide marketplace summary.
        """
        sellers = db.query(Seller).all()
        total_sellers = len(sellers)
        active_sellers = sum(1 for s in sellers if s.status == SellerStatus.APPROVED.value)
        pending_sellers = sum(1 for s in sellers if s.status == SellerStatus.PENDING.value)
        suspended_sellers = sum(1 for s in sellers if s.status == SellerStatus.SUSPENDED.value)

        total_products = db.query(Product).count()
        total_orders = db.query(Order).count()

        # Gross sales & commissions
        all_items = db.query(OrderItem).all()
        total_gmv = round(sum(i.total for i in all_items), 2)
        total_platform_cut = round(sum(i.total * 0.10 for i in all_items), 2)

        return {
            "total_sellers": total_sellers,
            "active_sellers": active_sellers,
            "pending_sellers": pending_sellers,
            "suspended_sellers": suspended_sellers,
            "total_catalog_products": total_products,
            "total_orders": total_orders,
            "gross_merchandise_volume": total_gmv,
            "platform_commission_revenue": total_platform_cut,
            "average_seller_rating": round(
                sum(float(s.rating or 5.0) for s in sellers) / max(1, total_sellers), 2
            ) if sellers else 5.0
        }
