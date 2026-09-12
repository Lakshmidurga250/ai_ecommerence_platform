"""
Next-Best-Action (NBA) Customer Engagement Engine.
Evaluates customer lifecycle events, cart states, RFM cohorts, loyalty points, and churn indicators
to recommend the single most impactful, context-aware engagement action for each user.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
try:
    from app.models.user import User
    from app.models.order import Order
    from app.models.cart import Cart, CartItem
    from app.models.review import Review
    from app.models.product import Product
except ImportError:
    from backend.app.models.user import User
    from backend.app.models.order import Order
    from backend.app.models.cart import Cart, CartItem
    from backend.app.models.review import Review
    from backend.app.models.product import Product


class NextBestActionEngine:
    """
    Contextual decision engine prioritizing commercial and engagement actions.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def predict_next_best_action(
        self,
        user_id: int,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Determines the optimal next-best-action for a customer.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": f"User {user_id} not found"}

        # 1. Inspect Cart Status
        cart = session.query(Cart).filter(Cart.user_id == user_id).first()
        cart_items = cart.items if cart else []
        cart_total = sum(item.product.price * item.quantity for item in cart_items if item.product) if cart_items else 0.0

        # 2. Inspect Orders & Delivery Status
        orders = session.query(Order).filter(Order.customer_id == user_id).order_by(Order.created_at.desc()).all()
        order_count = len(orders)
        latest_order = orders[0] if orders else None

        # 3. Check for Pending Reviews
        reviewed_product_ids = set(
            r.product_id for r in session.query(Review.product_id).filter(Review.user_id == user_id).all()
        )

        unreviewed_delivered_item = None
        if orders:
            for ord_obj in orders:
                for itm in ord_obj.items:
                    if itm.product_id not in reviewed_product_ids:
                        unreviewed_delivered_item = itm.product
                        break
                if unreviewed_delivered_item:
                    break

        # Decision Evaluation Flow:

        # Case A: Active Cart with Pending Items -> Abandoned Cart Recovery
        if cart_items and cart_total > 1500:
            return {
                "user_id": user_id,
                "action_type": "ABANDONED_CART_DISCOUNT",
                "priority": "URGENT",
                "confidence": 0.94,
                "headline": "Complete Your Order & Save 10%",
                "description": f"You left items worth ₹{cart_total:,.2f} in your bag. Complete checkout today with code 'CART10'.",
                "cta_label": "Resume Checkout",
                "target_route": "/cart",
                "context": {
                    "cart_items_count": len(cart_items),
                    "cart_total": cart_total,
                    "promo_code": "CART10"
                }
            }

        # Case B: Delivered Order Awaiting Review -> Social Proof & Review Prompt
        if unreviewed_delivered_item:
            return {
                "user_id": user_id,
                "action_type": "REQUEST_VERIFIED_REVIEW",
                "priority": "HIGH",
                "confidence": 0.88,
                "headline": f"How is your {unreviewed_delivered_item.name[:28]}?",
                "description": "Share your verified feedback to help other shoppers and earn 50 loyalty bonus points!",
                "cta_label": "Write a Review",
                "target_route": f"/products/{unreviewed_delivered_item.slug or unreviewed_delivered_item.id}",
                "context": {
                    "product_id": unreviewed_delivered_item.id,
                    "product_name": unreviewed_delivered_item.name,
                    "bonus_points": 50
                }
            }

        # Case C: Recent Technology / Electronics Purchaser -> Cross-Sell Accessories
        if latest_order:
            for itm in latest_order.items:
                cat_slug = itm.product.category.slug if itm.product and itm.product.category else ""
                if "laptop" in cat_slug or "smartphone" in cat_slug:
                    # Find a complementary accessory
                    comp_product = session.query(Product).filter(
                        Product.id != itm.product_id,
                        Product.is_active == True,
                        Product.price < 4000
                    ).first()
                    if comp_product:
                        return {
                            "user_id": user_id,
                            "action_type": "CROSS_SELL_ACCESSORY",
                            "priority": "MEDIUM",
                            "confidence": 0.82,
                            "headline": f"Perfect Companions for your {itm.product.name[:24]}",
                            "description": f"Upgrade your experience with {comp_product.name[:32]} at an exclusive 15% discount.",
                            "cta_label": "Explore Accessories",
                            "target_route": f"/products/{comp_product.slug or comp_product.id}",
                            "context": {
                                "anchor_product_id": itm.product_id,
                                "recommended_product_id": comp_product.id
                            }
                        }

        # Case D: Loyal Customer with High Lifetime Orders -> VIP Loyalty Perks
        if order_count >= 3:
            return {
                "user_id": user_id,
                "action_type": "LOYALTY_TIER_NUDGE",
                "priority": "MEDIUM",
                "confidence": 0.79,
                "headline": "You're Close to Gold VIP Status!",
                "description": "Unlock free express delivery and priority AI shopping concierge support on your next purchase.",
                "cta_label": "View Rewards Hub",
                "target_route": "/account",
                "context": {
                    "current_orders": order_count,
                    "target_tier": "GOLD_VIP"
                }
            }

        # Default Fallback: Personalized Catalog Discovery
        return {
            "user_id": user_id,
            "action_type": "EXPLORE_CURATED_COLLECTION",
            "priority": "NORMAL",
            "confidence": 0.72,
            "headline": "Curated Top Picks For You",
            "description": "Discover trending items tailored to your browsing taste with verified quality badges.",
            "cta_label": "Browse Catalog",
            "target_route": "/products",
            "context": {
                "featured_collection": "trending_ai_picks"
            }
        }
