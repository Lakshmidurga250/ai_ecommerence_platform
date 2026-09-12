"""
Customer Reviews & Ratings API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["Reviews & Ratings"])


@router.get("/product/{product_id}", response_model=List[ReviewRead])
def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve approved customer reviews with sentiment analysis scores."""
    return ReviewService.list_product_reviews(db, product_id, skip, limit)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def submit_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a verified review and rating; triggers automated AI sentiment pipeline."""
    return ReviewService.create_review(db, current_user.id, data)


@router.post("/{review_id}/helpful", response_model=ReviewRead)
def mark_review_helpful(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upvote review helpfulness."""
    return ReviewService.vote_helpful(db, review_id)
