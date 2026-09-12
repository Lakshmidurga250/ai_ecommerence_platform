"""
Session-Based Recommendation Engine.
Analyzes in-session sequential interaction clickstreams (views, clicks, dwell items)
using recency-weighted category transitions and item co-browsing probabilities.
"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
try:
    from app.models.product import Product
except ImportError:
    from backend.app.models.product import Product


class SessionRecommender:
    """
    Predicts next items of interest from active session interaction sequences.
    """

    # Category sequential transition likelihood matrix
    CATEGORY_TRANSITION_MATRIX = {
        "footwear-running": {"athletic-apparel": 0.45, "audio-wearables": 0.35, "footwear-running": 0.20},
        "athletic-apparel": {"footwear-running": 0.40, "audio-wearables": 0.35, "personal-care-grooming": 0.25},
        "laptops-computing": {"gaming-accessories": 0.50, "audio-wearables": 0.30, "laptops-computing": 0.20},
        "smartphones-tablets": {"audio-wearables": 0.55, "gaming-accessories": 0.25, "smartphones-tablets": 0.20},
        "audio-wearables": {"smartphones-tablets": 0.35, "athletic-apparel": 0.35, "laptops-computing": 0.30},
        "gaming-accessories": {"laptops-computing": 0.60, "audio-wearables": 0.40},
        "home-kitchen": {"home-kitchen": 0.40, "personal-care-grooming": 0.35, "books-stationery": 0.25},
        "personal-care-grooming": {"home-kitchen": 0.45, "athletic-apparel": 0.35, "personal-care-grooming": 0.20},
        "books-stationery": {"books-stationery": 0.45, "laptops-computing": 0.35, "home-kitchen": 0.20},
    }

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def recommend_for_session(
        self,
        session_product_ids: List[int],
        limit: int = 6,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Generates recommendations conditioned on the current browsing session.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        if not session_product_ids:
            # Fallback: Top rated catalog items
            fallback_items = session.query(Product).filter(Product.is_active == True).order_by(Product.rating.desc()).limit(limit).all()
            return {
                "session_items_analyzed": 0,
                "strategy": "FALLBACK_POPULAR",
                "recommendations": [self._format_item(p, 0.5, "Popular in Catalog") for p in fallback_items]
            }

        # Fetch session products in chronological order
        session_products = session.query(Product).filter(Product.id.in_(session_product_ids)).all()
        id_to_product = {p.id: p for p in session_products}
        ordered_products = [id_to_product[pid] for pid in session_product_ids if pid in id_to_product]

        if not ordered_products:
            fallback_items = session.query(Product).filter(Product.is_active == True).order_by(Product.rating.desc()).limit(limit).all()
            return {
                "session_items_analyzed": 0,
                "strategy": "FALLBACK_POPULAR",
                "recommendations": [self._format_item(p, 0.5, "Popular in Catalog") for p in fallback_items]
            }

        # Calculate recency-weighted category affinity: most recent items receive exponentially higher weight
        category_weights = defaultdict(float)
        alpha = 0.6  # Decay factor
        for idx, prod in enumerate(reversed(ordered_products)):
            weight = alpha ** idx
            cat_slug = prod.category.slug if prod.category else "general"
            category_weights[cat_slug] += weight

        # Most recent product defines immediate transition intent
        latest_product = ordered_products[-1]
        latest_cat = latest_product.category.slug if latest_product.category else "general"
        transitions = self.CATEGORY_TRANSITION_MATRIX.get(latest_cat, {})

        # Blend historical session category weight with immediate Markov transition
        blended_category_scores = defaultdict(float)
        for cat, weight in category_weights.items():
            blended_category_scores[cat] += weight * 0.4
        for next_cat, prob in transitions.items():
            blended_category_scores[next_cat] += prob * 0.6

        # Query candidates excluding already viewed products in session
        excluded_ids = set(session_product_ids)
        top_cats = sorted(blended_category_scores.keys(), key=lambda c: blended_category_scores[c], reverse=True)[:3]

        candidate_products = session.query(Product).join(Product.category).filter(
            Product.id.notin_(excluded_ids),
            Product.is_active == True
        ).all()

        scored_candidates = []
        for cand in candidate_products:
            cand_cat = cand.category.slug if cand.category else ""
            cat_score = blended_category_scores.get(cand_cat, 0.1)

            # Price similarity to recent session average
            avg_session_price = sum(p.price for p in ordered_products) / len(ordered_products)
            price_ratio = cand.price / max(1.0, avg_session_price)
            price_affinity = 1.0 / (1.0 + abs(price_ratio - 1.0))

            rating_factor = (cand.rating or 4.0) / 5.0
            total_score = 0.50 * cat_score + 0.30 * price_affinity + 0.20 * rating_factor

            reason = f"Complementary to your recent interest in {latest_product.name[:20]}"
            scored_candidates.append((cand, total_score, reason))

        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        top_picks = scored_candidates[:limit]

        return {
            "session_items_analyzed": len(ordered_products),
            "latest_viewed_product": {
                "id": latest_product.id,
                "name": latest_product.name,
                "category": latest_product.category.name if latest_product.category else ""
            },
            "strategy": "MARKOV_SESSION_TRANSITION",
            "recommendations": [
                self._format_item(cand, round(score, 3), reason)
                for cand, score, reason in top_picks
            ]
        }

    def _format_item(self, p: Product, score: float, reason: str) -> Dict[str, Any]:
        return {
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "price": p.price,
            "rating": p.rating,
            "image_url": (p.images[0].image_url if getattr(p, 'images', None) else getattr(p, 'image_url', '')) or '',
            "category": p.category.name if p.category else "General",
            "brand": p.brand.name if p.brand else "Generic",
            "session_affinity_score": score,
            "recommendation_reason": reason
        }
