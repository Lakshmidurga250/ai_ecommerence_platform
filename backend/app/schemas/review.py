"""
Review, Rating, and Sentiment Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    comment: str = Field(..., min_length=5, max_length=2000)


class ReviewSentimentRead(BaseModel):
    id: int
    sentiment_label: str  # POSITIVE, NEUTRAL, NEGATIVE
    polarity_score: float
    subjectivity_score: float
    confidence_score: float
    extracted_aspects: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


class ReviewRead(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    title: Optional[str] = None
    comment: str
    is_verified_purchase: bool
    status: str
    helpful_votes: int
    sentiment: Optional[ReviewSentimentRead] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewModerationUpdate(BaseModel):
    status: str  # APPROVED, REJECTED
