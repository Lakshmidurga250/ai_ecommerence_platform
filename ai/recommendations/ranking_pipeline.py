"""
Multi-Stage Production Recommendation Ranking Pipeline.
Architecture:
  Candidate Generation
          ↓
  Feature Engineering
          ↓
  Candidate Scoring
          ↓
  Business Rules Filter
          ↓
  Diversity Adjustment (MMR)
          ↓
  Final Ranking
"""

import math
from typing import Dict, Any, List, Optional, Set, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.catalog_expansion import UserRecentlyViewed
from ai.recommendations.neural_cf import NeuralCFEngine
from ai.recommendations.recommender import recommender_engine, RecommendationEngine


class RecommendationRankingPipeline:
    """
    Production-grade recommendation ranking pipeline with multi-stage candidate generation,
    feature engineering, business rules, and MMR diversity adjustment.
    """

    @classmethod
    def rank_for_user(
        cls,
        db: Session,
        user_id: Optional[int],
        limit: int = 10,
        category_id: Optional[int] = None,
        diversity_lambda: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Executes end-to-end ranking pipeline for authenticated user or anonymous guest.
        """
        # Stage 1: Candidate Generation
        candidates = cls._generate_candidates(db, user_id, category_id, pool_size=50)

        # Stage 2: Feature Engineering & User Context
        user_context = cls._extract_user_context(db, user_id)

        # Stage 3: Candidate Scoring
        scored_candidates = cls._score_candidates(db, candidates, user_context)

        # Stage 4: Business Rules Filter
        filtered_candidates = cls._apply_business_rules(db, scored_candidates, user_id)

        # Stage 5: Diversity Adjustment (Maximal Marginal Relevance - MMR)
        diverse_ranked = cls._apply_mmr_diversity(filtered_candidates, diversity_lambda, limit)

        # Format output
        results = []
        for prod, score, rank_factors in diverse_ranked:
            results.append({
                "product_id": prod.id,
                "name": prod.name,
                "slug": prod.slug,
                "price": prod.price,
                "compare_at_price": prod.compare_at_price,
                "rating": prod.rating,
                "review_count": prod.review_count,
                "stock": prod.stock,
                "category": prod.category.name if prod.category else "General",
                "category_id": prod.category_id,
                "brand": prod.brand.name if prod.brand else "Generic",
                "primary_image": prod.images[0].image_url if prod.images else None,
                "recommendation_score": round(score, 4),
                "ranking_rationale": rank_factors
            })

        return results

    @classmethod
    def rank_for_session(
        cls,
        db: Session,
        viewed_product_ids: List[int],
        limit: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Generates real-time session-based recommendations from active session browsing sequence.
        """
        if not viewed_product_ids:
            # Fallback to overall platform top-rated
            products = db.query(Product).filter(Product.is_active == True).order_by(desc(Product.rating), desc(Product.sales_count)).limit(limit).all()
            return [{
                "product_id": p.id,
                "name": p.name,
                "slug": p.slug,
                "price": p.price,
                "rating": p.rating,
                "category": p.category.name if p.category else "General",
                "brand": p.brand.name if p.brand else "Generic",
                "primary_image": p.images[0].image_url if p.images else None,
                "recommendation_score": 0.85,
                "ranking_rationale": ["Top Rated Platform Item"]
            } for p in products]

        # Extract target category from most recently viewed item
        last_id = viewed_product_ids[-1]
        last_prod = db.query(Product).filter(Product.id == last_id).first()
        target_cat_id = last_prod.category_id if last_prod else None

        q = db.query(Product).filter(
            Product.is_active == True,
            Product.stock > 0,
            ~Product.id.in_(viewed_product_ids)
        )
        if target_cat_id:
            q = q.filter(Product.category_id == target_cat_id)

        session_recs = q.order_by(desc(Product.rating), desc(Product.sales_count)).limit(limit).all()

        return [{
            "product_id": p.id,
            "name": p.name,
            "slug": p.slug,
            "price": p.price,
            "compare_at_price": p.compare_at_price,
            "rating": p.rating,
            "category": p.category.name if p.category else "General",
            "brand": p.brand.name if p.brand else "Generic",
            "primary_image": p.images[0].image_url if p.images else None,
            "recommendation_score": round(0.90 - (idx * 0.03), 2),
            "ranking_rationale": ["Session-Based Complementary", f"Matches viewed {last_prod.name[:15] if last_prod else 'items'}"]
        } for idx, p in enumerate(session_recs)]

    @classmethod
    def _generate_candidates(
        cls,
        db: Session,
        user_id: Optional[int],
        category_id: Optional[int],
        pool_size: int = 50
    ) -> List[Product]:
        """Stage 1: Multi-source candidate generation."""
        q = db.query(Product).filter(Product.is_active == True)
        if category_id:
            q = q.filter(Product.category_id == category_id)

        # Retrieve candidate pool
        candidates = q.order_by(desc(Product.is_featured), desc(Product.sales_count), desc(Product.rating)).limit(pool_size).all()
        return candidates

    @classmethod
    def _extract_user_context(cls, db: Session, user_id: Optional[int]) -> Dict[str, Any]:
        """Stage 2: Feature engineering on user interaction history."""
        if not user_id:
            return {"favorite_categories": set(), "average_spend": 5000.0, "purchased_ids": set()}

        # User's historical orders
        user_orders = db.query(Order).filter(Order.customer_id == user_id).all()
        purchased_ids = set()
        total_spend = 0.0
        fav_categories = set()

        for o in user_orders:
            total_spend += o.total_amount
            for item in o.items:
                purchased_ids.add(item.product_id)
                if item.product and item.product.category_id:
                    fav_categories.add(item.product.category_id)

        avg_spend = total_spend / len(user_orders) if user_orders else 5000.0

        return {
            "favorite_categories": fav_categories,
            "average_spend": avg_spend,
            "purchased_ids": purchased_ids
        }

    @classmethod
    def _score_candidates(
        cls,
        db: Session,
        candidates: List[Product],
        user_context: Dict[str, Any]
    ) -> List[Tuple[Product, float, List[str]]]:
        """Stage 3: Composite candidate scoring."""
        scored = []
        for prod in candidates:
            base_score = (prod.rating / 5.0) * 0.4  # Rating contribution (0.0 to 0.4)
            sales_boost = min(0.3, (prod.sales_count / 1000.0) * 0.3)  # Popularity (0.0 to 0.3)

            # Affinity bonus
            affinity_boost = 0.0
            reasons = []
            if prod.category_id in user_context["favorite_categories"]:
                affinity_boost += 0.2
                reasons.append("Category Affinity")
            if prod.is_featured:
                affinity_boost += 0.1
                reasons.append("Editor's Choice")

            # Price sensitivity alignment
            price_ratio = prod.price / max(1.0, user_context["average_spend"])
            if 0.5 <= price_ratio <= 2.0:
                affinity_boost += 0.1
                reasons.append("Matches Price Preference")

            if not reasons:
                reasons.append("Platform High Satisfaction")

            total_score = round(base_score + sales_boost + affinity_boost, 4)
            scored.append((prod, total_score, reasons))

        return scored

    @classmethod
    def _apply_business_rules(
        cls,
        db: Session,
        candidates: List[Tuple[Product, float, List[str]]],
        user_id: Optional[int]
    ) -> List[Tuple[Product, float, List[str]]]:
        """Stage 4: Business rules filtering (stock, recently purchased)."""
        recently_purchased = set()
        if user_id:
            user_orders = db.query(Order).filter(Order.customer_id == user_id).all()
            for o in user_orders:
                for it in o.items:
                    recently_purchased.add(it.product_id)

        filtered = []
        for prod, score, reasons in candidates:
            # Rule 1: Exclude out-of-stock items
            if prod.stock <= 0:
                continue
            # Rule 2: Suppress items customer already bought
            if prod.id in recently_purchased:
                continue

            filtered.append((prod, score, reasons))

        return filtered

    @classmethod
    def _apply_mmr_diversity(
        cls,
        candidates: List[Tuple[Product, float, List[str]]],
        diversity_lambda: float,
        limit: int
    ) -> List[Tuple[Product, float, List[str]]]:
        """
        Stage 5: Maximal Marginal Relevance (MMR) re-ranking.
        Balances high relevance score with brand and category diversity.
        """
        if len(candidates) <= limit:
            return sorted(candidates, key=lambda x: x[1], reverse=True)

        selected: List[Tuple[Product, float, List[str]]] = []
        remaining = list(candidates)

        while len(selected) < limit and remaining:
            best_idx = 0
            best_mmr = -float("inf")

            for idx, (cand_prod, cand_score, cand_reasons) in enumerate(remaining):
                relevance = cand_score

                # Compute maximum similarity to already selected items (shared brand/category)
                max_sim = 0.0
                for sel_prod, _, _ in selected:
                    sim = 0.0
                    if cand_prod.category_id == sel_prod.category_id:
                        sim += 0.5
                    if cand_prod.brand_id == sel_prod.brand_id:
                        sim += 0.5
                    if sim > max_sim:
                        max_sim = sim

                mmr_score = (diversity_lambda * relevance) - ((1.0 - diversity_lambda) * max_sim)
                if mmr_score > best_mmr:
                    best_mmr = mmr_score
                    best_idx = idx

            selected.append(remaining.pop(best_idx))

        return selected


# Alias for backward compatibility and multi-stage ranking suite
MultiStageRankingPipeline = RecommendationRankingPipeline
