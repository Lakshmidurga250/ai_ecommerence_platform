"""
Customer Reviews and AI Sentiment Analysis Models.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False, index=True)  # 1 to 5
    title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=False)
    is_verified_purchase = Column(Boolean, default=False, nullable=False)
    status = Column(String(30), default="APPROVED", nullable=False, index=True)  # PENDING, APPROVED, REJECTED
    helpful_votes = Column(Integer, default=0, nullable=False)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    sentiment = relationship("ReviewSentiment", back_populates="review", uselist=False, cascade="all, delete-orphan")


class ReviewSentiment(Base, TimestampMixin):
    __tablename__ = "review_sentiments"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), unique=True, nullable=False)
    sentiment_label = Column(String(30), nullable=False)  # POSITIVE, NEUTRAL, NEGATIVE
    polarity_score = Column(Float, nullable=False)  # -1.0 to 1.0
    subjectivity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    extracted_aspects = Column(JSON, default=dict, nullable=False)  # e.g., {"quality": "positive", "battery": "negative"}

    review = relationship("Review", back_populates="sentiment")
