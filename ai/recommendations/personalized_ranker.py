"""
Personalized Ranking Model (Learning-to-Rank Heuristic).
Personalizes product listings and search results for individual customers by synthesizing
category affinities, brand affinities, historical spending envelopes, and product quality scores.
"""
from typing import List, Dict, Any, Optional
import math
from collections import defaultdict
from sqlalchemy.orm import Session
try:
    from app.models.product import Product
    from app.models.order import Order
    from app.models.review import Review
except ImportError:
    from backend.app.models.product import Product
    from backend.app.models.order import Order
    from backend.app.models.review import Review


class PersonalizedRanker:
    """
    Ranks products according to individualized customer preferences and affinity signals.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def rank_products_for_user(
        self,
        products: List[Product],
        user_id: Optional[int] = None,
        limit: int = 20,
        db: Optional[Session] = None
    ) -> List[Dict[str, Any]]:
        """
        Re-ranks a candidate list of products tailored specifically for a customer.
        """
        session = db or self.db
        if not products:
            return []

        user_profile = self._build_user_profile(user_id, session) if user_id and session else None

        scored_products = []
        for p in products:
            score, explanation = self._score_product(p, user_profile)
            scored_products.append({
                "product": p,
                "personalized_score": round(score, 4),
                "ranking_reasons": explanation
            })

        # Sort descending by personalized score
        scored_products.sort(key=lambda x: x["personalized_score"], reverse=True)
        top_results = scored_products[:limit]

        formatted = []
        for idx, item in enumerate(top_results):
            prod = item["product"]
            formatted.append({
                "rank": idx + 1,
                "id": prod.id,
                "name": prod.name,
                "slug": prod.slug,
                "price": prod.price,
                "rating": prod.rating,
                "image_url": (prod.images[0].image_url if getattr(prod, 'images', None) else getattr(prod, 'image_url', '')) or '',
                "category": prod.category.name if prod.category else "Uncategorized",
                "category_slug": prod.category.slug if prod.category else "",
                "brand": prod.brand.name if prod.brand else "Generic",
                "brand_slug": prod.brand.slug if prod.brand else "",
                "personalized_score": item["personalized_score"],
                "ranking_reasons": item["ranking_reasons"]
            })

        return formatted

    def _build_user_profile(self, user_id: int, session: Session) -> Dict[str, Any]:
        """
        Extracts user preferences from past orders and reviews.
        """
        orders = session.query(Order).filter(Order.customer_id == user_id).all()
        category_counts = defaultdict(int)
        brand_counts = defaultdict(int)
        prices = []

        for ord_obj in orders:
            for item in ord_obj.items:
                p = item.product
                if p:
                    prices.append(p.price)
                    if p.category:
                        category_counts[p.category.slug] += 1
                    if p.brand:
                        brand_counts[p.brand.slug] += 1

        total_items = max(1, len(prices))
        category_affinities = {cat: count / total_items for cat, count in category_counts.items()}
        brand_affinities = {b: count / total_items for b, count in brand_counts.items()}

        median_spend = sorted(prices)[len(prices) // 2] if prices else 3000.0

        return {
            "category_affinities": category_affinities,
            "brand_affinities": brand_affinities,
            "median_spend": median_spend,
            "order_count": len(orders),
            "has_history": len(prices) > 0
        }

    def _score_product(self, product: Product, profile: Optional[Dict[str, Any]]) -> tuple[float, List[str]]:
        reasons = []

        # Baseline quality & rating factor (0.0 to 1.0)
        rating = product.rating or 4.0
        review_count = product.review_count or 0
        bayesian_rating = ((rating * review_count) + (4.0 * 5)) / (review_count + 5)
        quality_score = bayesian_rating / 5.0

        if not profile or not profile.get("has_history"):
            # Cold-start / anonymous user: rank primarily by quality & popularity
            if rating >= 4.5:
                reasons.append("Top Rated Catalog Item")
            return quality_score, reasons

        # 1. Category Affinity
        cat_slug = product.category.slug if product.category else ""
        cat_affinity = profile["category_affinities"].get(cat_slug, 0.0)
        if cat_affinity > 0.2:
            reasons.append(f"Matches your affinity for {product.category.name if product.category else 'this category'}")

        # 2. Brand Affinity
        brand_slug = product.brand.slug if product.brand else ""
        brand_affinity = profile["brand_affinities"].get(brand_slug, 0.0)
        if brand_affinity > 0.2:
            reasons.append(f"Favorite brand: {product.brand.name if product.brand else brand_slug}")

        # 3. Price Match Curve
        median_spend = profile["median_spend"]
        ratio = product.price / max(1.0, median_spend)
        # Gaussian curve centered at 1.0
        price_match = math.exp(-0.5 * ((ratio - 1.0) / 0.8) ** 2)
        if 0.7 <= ratio <= 1.3:
            reasons.append("Within your typical budget")

        # Weighted composition:
        # 30% Quality, 25% Category, 25% Brand, 20% Price Proximity
        composite_score = (
            0.30 * quality_score +
            0.25 * min(1.0, cat_affinity * 2.0) +
            0.25 * min(1.0, brand_affinity * 2.0) +
            0.20 * price_match
        )

        if not reasons:
            reasons.append("Trending product with high satisfaction score")

        return composite_score, reasons
