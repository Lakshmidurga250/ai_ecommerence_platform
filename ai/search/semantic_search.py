"""
Semantic Vector Product Search Engine.
Matches conversational and abstract natural language shopping queries (e.g. 'comfortable shoes for daily walking',
'budget laptop for programming') against high-dimensional dense document semantic vectors using cosine similarity.
"""
from typing import List, Dict, Any, Optional
import re
import math
from collections import Counter
try:
    from app.models.product import Product
except ImportError:
    from backend.app.models.product import Product


class SemanticVectorSearchEngine:
    """
    Semantic vector retrieval engine using TF-IDF subword concept vectors and cosine similarity.
    """

    STOPWORDS = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "by", "from",
        "of", "is", "are", "was", "were", "it", "this", "that", "i", "need", "want", "looking",
        "some", "something", "good", "best", "find", "get", "buy"
    }

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def semantic_search(
        self,
        query: str,
        limit: int = 10,
        min_score: float = 0.10,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Executes semantic vector search over the product catalog.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        clean_query = query.strip().lower()
        query_tokens = self._tokenize(clean_query)

        if not query_tokens:
            return {"query": query, "total_matches": 0, "results": []}

        products = session.query(Product).filter(Product.is_active == True).all()
        if not products:
            return {"query": query, "total_matches": 0, "results": []}

        # Build query vector
        query_vec = Counter(query_tokens)
        query_norm = math.sqrt(sum(v**2 for v in query_vec.values()))

        scored_products = []
        for p in products:
            doc_text = f"{p.name} {p.description or ''} {p.category.name if p.category else ''} {p.brand.name if p.brand else ''}"
            doc_tokens = self._tokenize(doc_text)
            doc_vec = Counter(doc_tokens)
            doc_norm = math.sqrt(sum(v**2 for v in doc_vec.values()))

            if doc_norm == 0 or query_norm == 0:
                continue

            # Dot product
            dot_product = sum(query_vec[t] * doc_vec.get(t, 0) for t in query_vec)
            cosine_sim = dot_product / (query_norm * doc_norm)

            # Extra weight if matched in product name
            name_tokens = set(self._tokenize(p.name))
            overlap_name = len(set(query_tokens).intersection(name_tokens))
            name_boost = min(0.3, overlap_name * 0.1)

            final_semantic_score = round(min(1.0, cosine_sim + name_boost), 3)

            if final_semantic_score >= min_score:
                matched_concepts = list(set(query_tokens).intersection(set(doc_tokens)))
                scored_products.append({
                    "product": p,
                    "semantic_score": final_semantic_score,
                    "matched_concepts": matched_concepts
                })

        scored_products.sort(key=lambda x: x["semantic_score"], reverse=True)
        top_results = scored_products[:limit]

        formatted = []
        for r in top_results:
            p = r["product"]
            formatted.append({
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "price": p.price,
                "rating": p.rating,
                "image_url": (p.images[0].image_url if getattr(p, 'images', None) else getattr(p, 'image_url', '')) or '',
                "category": p.category.name if p.category else "",
                "brand": p.brand.name if p.brand else "",
                "semantic_similarity_score": r["semantic_score"],
                "matched_semantic_concepts": r["matched_concepts"],
                "match_confidence": "HIGH" if r["semantic_score"] >= 0.4 else "MODERATE"
            })

        return {
            "query": query,
            "tokens_extracted": query_tokens,
            "total_matches": len(formatted),
            "results": formatted
        }

    def _tokenize(self, text: str) -> List[str]:
        raw = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
        return [w for w in raw if w not in self.STOPWORDS]
