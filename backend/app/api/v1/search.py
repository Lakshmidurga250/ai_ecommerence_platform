"""
Product Search API Endpoints with Lexical BM25 and Suggestions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_optional_current_user
from app.models.user import User
from app.schemas.product import ProductRead
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=List[ProductRead])
def search_products(
    q: str = Query("", description="Keywords or search query"),
    category_id: Optional[int] = Query(None),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Search products using BM25 relevance ranker / Elasticsearch."""
    user_id = current_user.id if current_user else None
    return SearchService.search(
        db=db,
        query_text=q,
        user_id=user_id,
        category_id=category_id,
        brand_id=brand_id,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        limit=limit
    )


@router.get("/suggestions", response_model=List[str])
def get_search_suggestions(
    prefix: str = Query(..., min_length=2, description="Query prefix to auto-complete"),
    db: Session = Depends(get_db)
):
    """Get fast auto-complete suggestions based on catalog inventory."""
    return SearchService.get_suggestions(db, prefix=prefix)
