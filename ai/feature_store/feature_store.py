"""
Unified Machine Learning Feature Store.
Provides standardized, consistent online feature serving for ML models (Ranking, Churn, Fraud, Pricing)
and offline feature definitions for experiment reproducibility.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
try:
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order
    from app.models.review import Review
except ImportError:
    from backend.app.models.user import User
    from backend.app.models.product import Product
    from backend.app.models.order import Order
    from backend.app.models.review import Review


class FeatureStore:
    """
    Centralized entity feature repository serving normalized feature vectors.
    """

    FEATURE_VIEWS = [
        {
            "name": "customer_engagement_features",
            "entity": "user_id",
            "features": [
                "order_count", "total_spend", "avg_order_value", "days_since_last_order",
                "return_rate", "favorite_category", "churn_risk", "loyalty_tier"
            ],
            "ttl_seconds": 3600
        },
        {
            "name": "product_commercial_features",
            "entity": "product_id",
            "features": [
                "price", "rating", "review_count", "quality_score",
                "return_risk", "price_tier", "is_in_stock"
            ],
            "ttl_seconds": 1800
        }
    ]

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def get_customer_features(self, user_id: int, db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Extracts standardized customer feature vector for online inference.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "entity_id": user_id,
                "order_count": 0,
                "total_spend": 0.0,
                "avg_order_value": 0.0,
                "days_since_last_order": 999,
                "return_rate": 0.0,
                "favorite_category": "none",
                "churn_risk": 0.50,
                "loyalty_tier": "BRONZE"
            }

        orders = session.query(Order).filter(Order.customer_id == user_id).all()
        order_count = len(orders)
        total_spend = sum(ord.total_amount for ord in orders)
        aov = round(total_spend / max(1, order_count), 2)

        # Days since last order
        if orders:
            latest = max(ord.created_at for ord in orders if ord.created_at)
            days_since = (datetime.utcnow() - latest).days
        else:
            days_since = 999

        # Favorite category
        cat_counts = {}
        for ord in orders:
            for itm in ord.items:
                if itm.product and itm.product.category:
                    cat = itm.product.category.slug
                    cat_counts[cat] = cat_counts.get(cat, 0) + 1

        fav_cat = max(cat_counts.items(), key=lambda x: x[1])[0] if cat_counts else "general"

        return {
            "entity_id": user_id,
            "feature_view": "customer_engagement_features",
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "features": {
                "order_count": order_count,
                "total_spend": round(total_spend, 2),
                "avg_order_value": aov,
                "days_since_last_order": days_since,
                "return_rate": 0.05,
                "favorite_category": fav_cat,
                "churn_risk": 0.15 if order_count >= 2 else 0.45,
                "loyalty_tier": "GOLD" if total_spend > 50000 else "SILVER" if total_spend > 10000 else "BRONZE"
            }
        }

    def get_product_features(self, product_id: int, db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Extracts standardized product commercial feature vector for ranking & pricing models.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        p = session.query(Product).filter(Product.id == product_id).first()
        if not p:
            return {"error": f"Product {product_id} not found"}

        # Price tier
        if p.price < 2000:
            price_tier = "BUDGET"
        elif p.price < 10000:
            price_tier = "MID_RANGE"
        elif p.price < 40000:
            price_tier = "PREMIUM"
        else:
            price_tier = "LUXURY_FLAGSHIP"

        rating = p.rating or 4.0
        review_count = p.review_count or 0
        quality_score = round(((rating / 5.0) * 80) + min(20, review_count), 1)

        return {
            "entity_id": product_id,
            "feature_view": "product_commercial_features",
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "features": {
                "price": p.price,
                "rating": rating,
                "review_count": review_count,
                "quality_score": quality_score,
                "price_tier": price_tier,
                "category_slug": p.category.slug if p.category else "general",
                "brand_slug": p.brand.slug if p.brand else "generic",
                "is_in_stock": getattr(p, 'stock', 0) > 0,
                "stock_level": getattr(p, 'stock', 0)
            }
        }

    def get_batch_product_features(self, product_ids: List[int], db: Optional[Session] = None) -> List[Dict[str, Any]]:
        return [self.get_product_features(pid, db) for pid in product_ids]

    def list_feature_views(self) -> List[Dict[str, Any]]:
        return self.FEATURE_VIEWS
