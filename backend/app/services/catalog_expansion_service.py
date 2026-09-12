"""
Catalog Expansion Service.
Provides business logic for:
- Product Bundles (Frequently Bought Together)
- Product Community Q&A
- Review Helpfulness Voting
- Recently Viewed Products Tracking
- Price & Back-in-Stock Alerts
- Product Comparison Matrices
- Inventory Stock Ledger
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.catalog_expansion import (
    ProductBundle, ProductQuestion, ProductAnswer,
    ReviewHelpfulnessVote, UserRecentlyViewed, PriceAlert, InventoryLedger
)
from app.models.product import Product
from app.models.review import Review


class CatalogExpansionService:

    # -------------------------------------------------------------------------
    # 1. Product Bundles
    # -------------------------------------------------------------------------
    @staticmethod
    def get_bundles_for_product(db: Session, product_id: int) -> List[Dict[str, Any]]:
        """Returns bundle pairings for a given primary product with savings calculation."""
        bundles = db.query(ProductBundle).filter(
            ProductBundle.primary_product_id == product_id,
            ProductBundle.is_active == True
        ).all()

        results = []
        for b in bundles:
            primary = b.primary_product
            bundled = b.bundle_product
            if not primary or not bundled:
                continue

            combined_regular_price = primary.price + bundled.price
            discount_amount = round(bundled.price * (b.discount_percent / 100.0), 2)
            bundle_price = round(combined_regular_price - discount_amount, 2)

            results.append({
                "bundle_id": b.id,
                "bundle_name": b.bundle_name,
                "discount_percent": b.discount_percent,
                "bundle_price": bundle_price,
                "regular_price": combined_regular_price,
                "savings": discount_amount,
                "primary_product": {
                    "id": primary.id,
                    "name": primary.name,
                    "price": primary.price,
                    "image": primary.images[0].image_url if primary.images else None
                },
                "bundled_product": {
                    "id": bundled.id,
                    "name": bundled.name,
                    "price": bundled.price,
                    "image": bundled.images[0].image_url if bundled.images else None
                }
            })
        return results

    @staticmethod
    def create_bundle(
        db: Session,
        primary_product_id: int,
        bundle_product_id: int,
        bundle_name: str,
        discount_percent: float = 10.0
    ) -> ProductBundle:
        bundle = ProductBundle(
            primary_product_id=primary_product_id,
            bundle_product_id=bundle_product_id,
            bundle_name=bundle_name,
            discount_percent=discount_percent,
            is_active=True
        )
        db.add(bundle)
        db.commit()
        db.refresh(bundle)
        return bundle

    # -------------------------------------------------------------------------
    # 2. Product Q&A
    # -------------------------------------------------------------------------
    @staticmethod
    def get_questions_for_product(db: Session, product_id: int) -> List[Dict[str, Any]]:
        questions = db.query(ProductQuestion).filter(
            ProductQuestion.product_id == product_id,
            ProductQuestion.is_approved == True
        ).order_by(desc(ProductQuestion.created_at)).all()

        return [
            {
                "id": q.id,
                "question": q.question_text,
                "asked_by": q.user.username if q.user else "Anonymous Customer",
                "created_at": q.created_at.isoformat(),
                "is_answered": len(q.answers) > 0,
                "answers": [
                    {
                        "id": a.id,
                        "answer": a.answer_text,
                        "answered_by": a.user.username if a.user else "Verified Seller",
                        "is_seller_reply": a.is_seller_reply,
                        "created_at": a.created_at.isoformat()
                    }
                    for a in q.answers if a.is_approved
                ]
            }
            for q in questions
        ]

    @staticmethod
    def ask_question(db: Session, product_id: int, user_id: int, question_text: str) -> ProductQuestion:
        q = ProductQuestion(
            product_id=product_id,
            user_id=user_id,
            question_text=question_text,
            is_approved=True
        )
        db.add(q)
        db.commit()
        db.refresh(q)
        return q

    @staticmethod
    def answer_question(
        db: Session,
        question_id: int,
        user_id: int,
        answer_text: str,
        is_seller_reply: bool = False
    ) -> ProductAnswer:
        ans = ProductAnswer(
            question_id=question_id,
            user_id=user_id,
            answer_text=answer_text,
            is_seller_reply=is_seller_reply,
            is_approved=True
        )
        q = db.query(ProductQuestion).filter(ProductQuestion.id == question_id).first()
        if q:
            q.is_answered = True
        db.add(ans)
        db.commit()
        db.refresh(ans)
        return ans

    # -------------------------------------------------------------------------
    # 3. Review Helpfulness Voting
    # -------------------------------------------------------------------------
    @staticmethod
    def vote_review(db: Session, review_id: int, user_id: int, is_helpful: bool = True) -> Dict[str, Any]:
        existing_vote = db.query(ReviewHelpfulnessVote).filter(
            ReviewHelpfulnessVote.review_id == review_id,
            ReviewHelpfulnessVote.user_id == user_id
        ).first()

        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ValueError(f"Review {review_id} not found")

        if existing_vote:
            if existing_vote.is_helpful != is_helpful:
                existing_vote.is_helpful = is_helpful
                review.helpful_votes = max(0, review.helpful_votes + (1 if is_helpful else -1))
        else:
            vote = ReviewHelpfulnessVote(review_id=review_id, user_id=user_id, is_helpful=is_helpful)
            db.add(vote)
            if is_helpful:
                review.helpful_votes += 1

        db.commit()
        db.refresh(review)

        total_helpful = db.query(ReviewHelpfulnessVote).filter(
            ReviewHelpfulnessVote.review_id == review_id,
            ReviewHelpfulnessVote.is_helpful == True
        ).count()
        total_unhelpful = db.query(ReviewHelpfulnessVote).filter(
            ReviewHelpfulnessVote.review_id == review_id,
            ReviewHelpfulnessVote.is_helpful == False
        ).count()

        return {
            "review_id": review_id,
            "helpful_votes": total_helpful,
            "unhelpful_votes": total_unhelpful,
            "user_voted": is_helpful
        }

    # -------------------------------------------------------------------------
    # 4. Recently Viewed Products
    # -------------------------------------------------------------------------
    @staticmethod
    def record_recently_viewed(db: Session, user_id: int, product_id: int):
        existing = db.query(UserRecentlyViewed).filter(
            UserRecentlyViewed.user_id == user_id,
            UserRecentlyViewed.product_id == product_id
        ).first()

        if existing:
            existing.viewed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        else:
            rv = UserRecentlyViewed(user_id=user_id, product_id=product_id)

            db.add(rv)
        db.commit()

    @staticmethod
    def get_recently_viewed(db: Session, user_id: int, limit: int = 10) -> List[Product]:
        recent = db.query(UserRecentlyViewed).filter(
            UserRecentlyViewed.user_id == user_id
        ).order_by(desc(UserRecentlyViewed.viewed_at)).limit(limit).all()

        product_ids = [r.product_id for r in recent]
        if not product_ids:
            return []

        # Maintain recency ordering
        products = {p.id: p for p in db.query(Product).filter(Product.id.in_(product_ids)).all()}
        return [products[pid] for pid in product_ids if pid in products]

    # -------------------------------------------------------------------------
    # 5. Price Alerts
    # -------------------------------------------------------------------------
    @staticmethod
    def create_price_alert(
        db: Session,
        user_id: int,
        product_id: int,
        target_price: float,
        alert_type: str = "PRICE_DROP"
    ) -> PriceAlert:
        alert = PriceAlert(
            user_id=user_id,
            product_id=product_id,
            target_price=target_price,
            alert_type=alert_type
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_user_alerts(db: Session, user_id: int) -> List[Dict[str, Any]]:
        alerts = db.query(PriceAlert).filter(PriceAlert.user_id == user_id).all()
        return [
            {
                "id": a.id,
                "product_id": a.product_id,
                "product_name": a.product.name if a.product else f"Product #{a.product_id}",
                "target_price": a.target_price,
                "current_price": a.product.price if a.product else 0.0,
                "alert_type": a.alert_type,
                "is_triggered": a.is_triggered,
                "created_at": a.created_at.isoformat()
            }
            for a in alerts
        ]

    # -------------------------------------------------------------------------
    # 6. Inventory Ledger Tracking
    # -------------------------------------------------------------------------
    @staticmethod
    def record_stock_ledger_movement(
        db: Session,
        product_id: int,
        transaction_type: str,
        quantity_change: int,
        reference_id: Optional[str] = None,
        notes: Optional[str] = None,
        warehouse_id: Optional[int] = None
    ) -> InventoryLedger:
        """Records an atomic stock movement entry in the immutable inventory ledger."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        new_balance = max(0, product.stock + quantity_change)
        product.stock = new_balance

        entry = InventoryLedger(
            product_id=product_id,
            warehouse_id=warehouse_id,
            transaction_type=transaction_type,
            quantity_change=quantity_change,
            balance_after=new_balance,
            reference_id=reference_id,
            notes=notes
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_product_ledger(db: Session, product_id: int, limit: int = 50) -> List[InventoryLedger]:
        return db.query(InventoryLedger).filter(
            InventoryLedger.product_id == product_id
        ).order_by(desc(InventoryLedger.created_at)).limit(limit).all()
