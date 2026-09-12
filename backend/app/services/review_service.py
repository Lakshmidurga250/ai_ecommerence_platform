"""
Customer Review & AI Sentiment Processing Service.
Computes real sentiment analysis scores and updates product aggregate ratings.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.exceptions import NotFoundException, ConflictException, AppException
from app.models.review import Review, ReviewSentiment
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.schemas.review import ReviewCreate
from ai.sentiment.analyzer import SentimentAnalyzer


class ReviewService:
    @staticmethod
    def create_review(db: Session, user_id: int, data: ReviewCreate) -> Review:
        product = db.query(Product).filter(Product.id == data.product_id).first()
        if not product:
            raise NotFoundException("Product", str(data.product_id))

        # Check if user previously purchased this product for verified purchase flag
        verified = db.query(OrderItem).join(Order).filter(
            Order.customer_id == user_id,
            OrderItem.product_id == data.product_id,
            Order.status == "DELIVERED"
        ).first() is not None

        # Create review
        review = Review(
            product_id=data.product_id,
            user_id=user_id,
            rating=data.rating,
            title=data.title,
            comment=data.comment,
            is_verified_purchase=verified,
            status="APPROVED",
            helpful_votes=0
        )
        db.add(review)
        db.flush()

        # Run mathematical Sentiment Analysis
        sentiment_res = SentimentAnalyzer.analyze_text(f"{data.title or ''} {data.comment}")
        sentiment = ReviewSentiment(
            review_id=review.id,
            sentiment_label=sentiment_res["sentiment_label"],
            polarity_score=sentiment_res["polarity_score"],
            subjectivity_score=sentiment_res["subjectivity_score"],
            confidence_score=sentiment_res["confidence_score"],
            extracted_aspects=sentiment_res["extracted_aspects"]
        )
        db.add(sentiment)

        # Update product aggregate rating and review count
        stats = db.query(
            func.avg(Review.rating).label("avg_rating"),
            func.count(Review.id).label("total_reviews")
        ).filter(Review.product_id == data.product_id, Review.status == "APPROVED").first()

        if stats:
            product.rating = round(float(stats.avg_rating or data.rating), 2)
            product.review_count = int(stats.total_reviews or 1)

        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def list_product_reviews(db: Session, product_id: int, skip: int = 0, limit: int = 50) -> List[Review]:
        return db.query(Review).filter(
            Review.product_id == product_id,
            Review.status == "APPROVED"
        ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def vote_helpful(db: Session, review_id: int) -> Review:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise NotFoundException("Review", str(review_id))
        review.helpful_votes += 1
        db.commit()
        db.refresh(review)
        return review
