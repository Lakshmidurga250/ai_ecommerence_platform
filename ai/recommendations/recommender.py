"""
Multi-Level Recommendation Engine (Levels 1 to 5).
Includes:
- Level 1: Popularity & Trending (Bayesian dampening)
- Level 2: Content-Based Filtering (TF-IDF & Cosine Similarity)
- Level 3: Collaborative Filtering (User-Item neighborhood matrix)
- Level 4: Hybrid Recommender (Weighted ensemble with explainability reasons)
- Level 5: Matrix Factorization Latent Embeddings Recommender
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
        self.product_tfidf_matrix = None
        self.product_id_to_idx: Dict[int, int] = {}
        self.idx_to_product_id: Dict[int, int] = {}
        
        # User-Item Interaction Matrix for Collaborative Filtering
        self.user_item_matrix: Dict[int, Dict[int, float]] = defaultdict(dict)  # user_id -> {prod_id: weight}
        self.item_user_matrix: Dict[int, Dict[int, float]] = defaultdict(dict)  # prod_id -> {user_id: weight}

    # =========================================================================
    # LEVEL 1: POPULARITY & TRENDING
    # =========================================================================
    @staticmethod
    def get_popularity_recommendations(products: List[Any], limit: int = 10) -> List[Tuple[int, float, str]]:
        """
        Bayesian dampened popularity score:
        Score = (R * v + C * m) / (v + m) * log(1 + sales_count)
        where R = product rating, v = review count, m = 5 (prior count threshold), C = 4.0 (prior mean).
        """
        prior_m = 5.0
        prior_c = 4.0
        scored = []

        for p in products:
            v = float(getattr(p, "review_count", 0))
            r = float(getattr(p, "rating", 0.0))
            sales = float(getattr(p, "sales_count", 0))

            bayesian_rating = (r * v + prior_c * prior_m) / (v + prior_m)
            popularity_score = round(bayesian_rating * math.log1p(sales + 1), 3)

            scored.append((p.id, popularity_score, "Trending & Popular across the marketplace"))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]

    # =========================================================================
    # LEVEL 2: CONTENT-BASED FILTERING (TF-IDF + COSINE SIMILARITY)
    # =========================================================================
    def fit_content_model(self, products: List[Any]):
        """Fit TF-IDF matrix over product title, description, category, brand, and attributes."""
        if not products:
            return

        corpus = []
        self.product_id_to_idx.clear()
        self.idx_to_product_id.clear()

        for idx, p in enumerate(products):
            self.product_id_to_idx[p.id] = idx
            self.idx_to_product_id[idx] = p.id

            cat_name = p.category.name if getattr(p, "category", None) else ""
            brand_name = p.brand.name if getattr(p, "brand", None) else ""
            attr_text = " ".join(f"{k} {v}" for k, v in (getattr(p, "attributes", {}) or {}).items())

            doc = f"{p.name} {p.name} {cat_name} {cat_name} {brand_name} {p.description or ''} {attr_text}"
            corpus.append(doc)

        try:
            self.product_tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
        except Exception:
            self.product_tfidf_matrix = None

    def get_content_recommendations(self, target_product_id: int, limit: int = 10) -> List[Tuple[int, float, str]]:
        """Find products similar in attributes and content to the target product."""
        if self.product_tfidf_matrix is None or target_product_id not in self.product_id_to_idx:
            return []

        target_idx = self.product_id_to_idx[target_product_id]
        target_vec = self.product_tfidf_matrix[target_idx]

        sim_scores = cosine_similarity(target_vec, self.product_tfidf_matrix).flatten()
        sim_scores[target_idx] = -1.0  # Exclude target product itself

        top_indices = np.argsort(sim_scores)[::-1][:limit]
        results = []
        for idx in top_indices:
            score = float(sim_scores[idx])
            if score > 0.05:
                prod_id = self.idx_to_product_id[idx]
                results.append((prod_id, round(score, 3), "Similar product with matching specifications and features"))

        return results

    # =========================================================================
    # LEVEL 3: COLLABORATIVE FILTERING (USER-ITEM INTERACTION MATRIX)
    # =========================================================================
    def record_interaction(self, user_id: int, product_id: int, event_type: str):
        """Record user behavioral signals with appropriate interaction weights."""
        weight_map = {
            "VIEW": 1.0,
            "CLICK": 1.5,
            "WISHLIST": 3.0,
            "CART_ADD": 4.0,
            "PURCHASE": 10.0,
            "RATING_5": 5.0,
            "RATING_4": 4.0
        }
        w = weight_map.get(event_type.upper(), 1.0)
        self.user_item_matrix[user_id][product_id] = self.user_item_matrix[user_id].get(product_id, 0.0) + w
        self.item_user_matrix[product_id][user_id] = self.item_user_matrix[product_id].get(user_id, 0.0) + w

    def get_collaborative_recommendations(self, user_id: int, limit: int = 10) -> List[Tuple[int, float, str]]:
        """Item-Item collaborative filtering based on co-occurrence in user histories."""
        user_items = self.user_item_matrix.get(user_id, {})
        if not user_items:
            return []

        candidate_scores = defaultdict(float)

        for user_prod_id, user_weight in user_items.items():
            # Find users who also interacted with user_prod_id
            co_users = self.item_user_matrix.get(user_prod_id, {})
            for other_user, other_weight in co_users.items():
                if other_user == user_id:
                    continue
                # Other items interacted by other_user
                for candidate_prod_id, cand_weight in self.user_item_matrix.get(other_user, {}).items():
                    if candidate_prod_id in user_items:
                        continue  # Already interacted
                    co_score = min(user_weight, other_weight) * cand_weight
                    candidate_scores[candidate_prod_id] += co_score

        if not candidate_scores:
            return []

        max_val = max(candidate_scores.values()) or 1.0
        results = [
            (pid, round(score / max_val, 3), "Customers with similar shopping habits also bought or viewed this")
            for pid, score in sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        ]
        return results

    # =========================================================================
    # LEVEL 4: HYBRID RECOMMENDATION PIPELINE
    # =========================================================================
    def get_hybrid_recommendations(
        self,
        user_id: Optional[int],
        all_products: List[Any],
        recent_product_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Tuple[int, float, str, str]]:
        """
        Ensemble hybrid recommender:
        Weights: Collaborative (45%), Content-Based (35%), Popularity (20%).
        Gracefully resolves cold-start for new users or unseen products.
        Returns: [(product_id, score, explanation, model_type)]
        """
        # Ensure content model is fit
        if self.product_tfidf_matrix is None and all_products:
            self.fit_content_model(all_products)

        final_scores: Dict[int, float] = defaultdict(float)
        explanations: Dict[int, str] = {}
        model_types: Dict[int, str] = {}

        # 1. Collaborative signals
        cf_recs = self.get_collaborative_recommendations(user_id, limit=limit * 2) if user_id else []
        for pid, score, expl in cf_recs:
            final_scores[pid] += 0.45 * score
            explanations[pid] = expl
            model_types[pid] = "COLLABORATIVE"

        # 2. Content-based signals
        target_pid = recent_product_id
        if not target_pid and user_id and self.user_item_matrix.get(user_id):
            # Use most interacted product
            target_pid = max(self.user_item_matrix[user_id].items(), key=lambda x: x[1])[0]

        if target_pid:
            content_recs = self.get_content_recommendations(target_pid, limit=limit * 2)
            for pid, score, expl in content_recs:
                final_scores[pid] += 0.35 * score
                if pid not in explanations:
                    explanations[pid] = "Recommended because you viewed similar products"
                    model_types[pid] = "CONTENT"

        # 3. Popularity baseline dampener
        pop_recs = self.get_popularity_recommendations(all_products, limit=limit * 2)
        max_pop = pop_recs[0][1] if pop_recs else 1.0
        for pid, score, expl in pop_recs:
            norm_pop = score / max_pop
            final_scores[pid] += 0.20 * norm_pop
            if pid not in explanations:
                explanations[pid] = expl
                model_types[pid] = "POPULARITY"

        # Sort and produce top recommendations
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [
            (pid, round(score, 3), explanations.get(pid, "Recommended for you"), model_types.get(pid, "HYBRID"))
            for pid, score in ranked
        ]

    # =========================================================================
    # LEVEL 5: LATENT MATRIX FACTORIZATION / EMBEDDING SIMILARITY
    # =========================================================================
    def get_matrix_factorization_recommendations(
        self,
        user_id: int,
        all_products: List[Any],
        embedding_dim: int = 16,
        limit: int = 10
    ) -> List[Tuple[int, float, str]]:
        """
        Latent Factor SVD Decomposition on user-item interaction signals.
        Computes dense user and item representation vectors and ranks by dot-product.
        """
        if not self.user_item_matrix or user_id not in self.user_item_matrix:
            return []

        user_ids = list(self.user_item_matrix.keys())
        product_ids = [p.id for p in all_products]

        u_map = {uid: i for i, uid in enumerate(user_ids)}
        p_map = {pid: j for j, pid in enumerate(product_ids)}

        matrix = np.zeros((len(user_ids), len(product_ids)))
        for u, items in self.user_item_matrix.items():
            for p, w in items.items():
                if p in p_map:
                    matrix[u_map[u], p_map[p]] = w

        if matrix.shape[0] < 2 or matrix.shape[1] < 2:
            return []

        try:
            k = min(embedding_dim, matrix.shape[0] - 1, matrix.shape[1] - 1)
            u_vecs, s_vals, vt_vecs = np.linalg.svd(matrix, full_matrices=False)
            u_factors = u_vecs[:, :k] * np.sqrt(s_vals[:k])
            p_factors = (vt_vecs[:k, :].T) * np.sqrt(s_vals[:k])

            target_user_vec = u_factors[u_map[user_id]]
            predicted_scores = np.dot(p_factors, target_user_vec)

            # Exclude already interacted
            user_interacted = set(self.user_item_matrix[user_id].keys())
            ranked_indices = np.argsort(predicted_scores)[::-1]

            results = []
            for idx in ranked_indices:
                pid = product_ids[idx]
                if pid not in user_interacted:
                    norm_score = max(0.0, min(1.0, float(predicted_scores[idx]) / (np.max(predicted_scores) or 1.0)))
                    results.append((pid, round(norm_score, 3), "Personalized recommendation from Neural Latent Factorization"))
                    if len(results) >= limit:
                        break
            return results
        except Exception:
            return []


# Global Recommender Instance
recommender_engine = RecommendationEngine()
