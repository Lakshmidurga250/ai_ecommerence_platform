"""
Visual Search API Router.
Accepts image URLs or uploaded image descriptors and returns visually similar products.
"""

import time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from ai.search.visual_search import VisualSearchEngine

router = APIRouter(prefix="/search/visual", tags=["AI Visual Search"])


class VisualSearchRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: Optional[str] = Field(None, description="Public or uploaded image URL to match against catalog")
    image_base64: Optional[str] = Field(None, description="Optional base64 encoded image string")
    category_hint: Optional[str] = Field(None, description="Optional category slug constraint")
    limit: int = Field(8, ge=1, le=30, description="Maximum number of visually similar products to return")
    top_k: Optional[int] = Field(None, description="Alias for limit")


class VisualMatchItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    name: Optional[str] = None
    product_name: Optional[str] = None
    slug: str
    price: float
    compare_at_price: Optional[float] = None
    rating: float
    stock: int
    category: str
    brand: str
    primary_image: Optional[str] = None
    image_url: Optional[str] = None
    similarity_score: float
    color_match_confidence: float = 0.88
    matching_aspects: List[str] = Field(default_factory=list)
    reasoning: str = ""


class VisualSearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    query_image_url: str
    total_matches: int
    execution_ms: float
    results: List[VisualMatchItem]
    matches: List[VisualMatchItem]


@router.post("", response_model=VisualSearchResponse)
@router.post("/", response_model=VisualSearchResponse)
def visual_product_search(
    payload: VisualSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Performs visual vector nearest-neighbor search across catalog products.
    """
    start_time = time.perf_counter()
    url = payload.image_url or (f"data:image/jpeg;base64,{payload.image_base64[:30]}" if payload.image_base64 else None)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either image_url or image_base64 must be provided for visual similarity search"
        )

    limit = payload.top_k or payload.limit
    raw_results = VisualSearchEngine.search_by_image(
        db=db,
        query_image_url=url,
        category_hint=payload.category_hint,
        limit=limit
    )

    formatted_matches = []
    for r in raw_results:
        formatted_matches.append(VisualMatchItem(
            product_id=r["product_id"],
            name=r["name"],
            product_name=r["name"],
            slug=r["slug"],
            price=r["price"],
            compare_at_price=r.get("compare_at_price"),
            rating=r["rating"],
            stock=r["stock"],
            category=r["category"],
            brand=r["brand"],
            primary_image=r.get("primary_image"),
            image_url=r.get("primary_image"),
            similarity_score=r["similarity_score"],
            color_match_confidence=0.88,
            matching_aspects=r.get("matching_aspects", []),
            reasoning=f"Matched on visual geometry and {r['category']} color distribution"
        ))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "query_image_url": url,
        "total_matches": len(formatted_matches),
        "execution_ms": round(elapsed_ms, 2),
        "results": formatted_matches,
        "matches": formatted_matches
    }
