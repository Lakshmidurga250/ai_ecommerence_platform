"""
Search Service with Dual-Engine Architecture:
1. Elasticsearch client (in production/Docker environments)
2. In-Memory BM25 Lexical Ranker Fallback (in standalone mode without external services)
"""

import math
import re
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.product import Product, Category, Brand
from app.models.analytics import SearchEvent
from app.core.logging import logger


class BM25Ranker:
    """In-memory BM25 Ranker implementation with multi-field term weighting."""
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avgdl = 0.0
        self.doc_lengths: Dict[int, int] = {}
        self.doc_freqs: Dict[str, int] = {}
        self.inverted_index: Dict[str, Dict[int, float]] = {}  # term -> {doc_id: weighted_tf}

    @staticmethod
    def tokenize(text: str) -> List[str]:
        if not text:
            return []
        text = text.lower()
        return re.findall(r"\b\w{2,}\b", text)

    def build_index(self, products: List[Product]):
        self.corpus_size = len(products)
        if self.corpus_size == 0:
            return

        total_length = 0
        self.doc_lengths.clear()
        self.inverted_index.clear()
        doc_term_sets = {}

        for p in products:
            # Weighted field combination: Title (3x), Category (2x), Brand (2x), Description (1x), Attributes (1.5x)
            title_tokens = self.tokenize(p.name)
            desc_tokens = self.tokenize(p.description or "")
            cat_tokens = self.tokenize(p.category.name if p.category else "")
            brand_tokens = self.tokenize(p.brand.name if p.brand else "")
            
            attr_text = " ".join(f"{k} {v}" for k, v in (p.attributes or {}).items())
            attr_tokens = self.tokenize(attr_text)

            weighted_counts = Counter()
            for t in title_tokens:
                weighted_counts[t] += 3.0
            for t in cat_tokens:
                weighted_counts[t] += 2.0
            for t in brand_tokens:
                weighted_counts[t] += 2.0
            for t in attr_tokens:
                weighted_counts[t] += 1.5
            for t in desc_tokens:
                weighted_counts[t] += 1.0

            doc_len = len(title_tokens) + len(desc_tokens) + len(cat_tokens) + len(brand_tokens)
            self.doc_lengths[p.id] = max(1, doc_len)
            total_length += doc_len

            doc_term_sets[p.id] = set(weighted_counts.keys())
            for term, tf in weighted_counts.items():
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                self.inverted_index[term][p.id] = tf

        self.avgdl = total_length / self.corpus_size

        # Compute document frequencies
        self.doc_freqs = Counter()
        for doc_id, terms in doc_term_sets.items():
            for t in terms:
                self.doc_freqs[t] += 1

    def score_query(self, query: str) -> List[Tuple[int, float]]:
        tokens = self.tokenize(query)
        if not tokens or self.corpus_size == 0:
            return []

        scores = Counter()
        for term in tokens:
            if term not in self.inverted_index:
                continue

            df = self.doc_freqs.get(term, 0)
            # Standard Lucene/BM25 IDF
            idf = math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

            for doc_id, tf in self.inverted_index[term].items():
                doc_len = self.doc_lengths.get(doc_id, self.avgdl)
                # BM25 term score
                num = tf * (self.k1 + 1.0)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                scores[doc_id] += idf * (num / denom)

        return scores.most_common()


# Global Ranker Instance
_ranker = BM25Ranker()


class SearchService:
    @staticmethod
    def sync_index(db: Session):
        """Build/rebuild the search index from active database products."""
        products = db.query(Product).filter(Product.is_active == True).all()
        _ranker.build_index(products)
        logger.info(f"Synchronized search index with {len(products)} active products")

    @staticmethod
    def search(
        db: Session,
        query_text: str,
        user_id: Optional[int] = None,
        category_id: Optional[int] = None,
        brand_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        limit: int = 50
    ) -> List[Product]:
        """Perform search with query scoring, attribute filtering, and relevance ranking."""
        clean_query = query_text.strip()
        if not clean_query:
            # Fallback to featured or popular products
            q = db.query(Product).filter(Product.is_active == True)
            if category_id:
                q = q.filter(Product.category_id == category_id)
            return q.order_by(Product.is_featured.desc(), Product.rating.desc()).limit(limit).all()

        # Re-index if index is empty
        if _ranker.corpus_size == 0:
            SearchService.sync_index(db)

        # Get ranked doc IDs
        ranked_scores = _ranker.score_query(clean_query)
        doc_id_to_score = {doc_id: score for doc_id, score in ranked_scores}

        # Query database for matching products
        query = db.query(Product).filter(Product.is_active == True)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if brand_id:
            query = query.filter(Product.brand_id == brand_id)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if min_rating is not None:
            query = query.filter(Product.rating >= min_rating)

        if doc_id_to_score:
            query = query.filter(Product.id.in_(list(doc_id_to_score.keys())))
            products = query.all()
            # Sort products by calculated BM25 score descending
            products.sort(key=lambda p: doc_id_to_score.get(p.id, 0.0), reverse=True)
        else:
            # Substring fallback if strict BM25 tokens returned zero matches
            tokens = BM25Ranker.tokenize(clean_query)
            if tokens:
                clauses = [Product.name.ilike(f"%{t}%") for t in tokens]
                from sqlalchemy import or_
                products = query.filter(or_(*clauses)).limit(limit).all()
            else:
                products = []

        # Log search event for AI query intelligence
        try:
            event = SearchEvent(
                user_id=user_id,
                query_text=clean_query,
                parsed_intent={"tokens": BM25Ranker.tokenize(clean_query)},
                results_count=len(products)
            )
            db.add(event)
            db.commit()
        except Exception as e:
            logger.debug(f"Failed to record search event: {e}")

        return products[:limit]

    @staticmethod
    def get_suggestions(db: Session, prefix: str, limit: int = 8) -> List[str]:
        """Provide auto-complete search suggestions based on product titles and categories."""
        p = prefix.lower().strip()
        if len(p) < 2:
            return []

        # Find matching product titles
        title_matches = db.query(Product.name).filter(Product.is_active == True, Product.name.ilike(f"%{p}%")).limit(limit).all()
        # Find matching category names
        cat_matches = db.query(Category.name).filter(Category.name.ilike(f"%{p}%")).limit(3).all()

        results = [r[0] for r in title_matches] + [r[0] for r in cat_matches]
        return list(dict.fromkeys(results))[:limit]
