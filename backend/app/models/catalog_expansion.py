"""
Catalog Expansion, Customer Experience, and Inventory Ledger Models.
Extends relational foundation with:
- Product Bundles & Frequently Bought Together
- Product Q&A (Questions & Verified Answers)
- Review Helpfulness Voting
- User Recently Viewed History
- Price & Back-in-Stock Alerts
- Inventory Stock Ledger with atomic movements
- Seller Payouts & Commission tracking
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class ProductBundle(Base, TimestampMixin):
    __tablename__ = "product_bundles"

    id = Column(Integer, primary_key=True, index=True)
    primary_product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    bundle_product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    bundle_name = Column(String(150), nullable=False)
    discount_percent = Column(Float, default=10.0)
    is_active = Column(Boolean, default=True)

    primary_product = relationship("Product", foreign_keys=[primary_product_id])
    bundle_product = relationship("Product", foreign_keys=[bundle_product_id])


class ProductQuestion(Base, TimestampMixin):
    __tablename__ = "product_questions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    is_answered = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)

    product = relationship("Product")
    user = relationship("User")
    answers = relationship("ProductAnswer", back_populates="question", cascade="all, delete-orphan")


class ProductAnswer(Base, TimestampMixin):
    __tablename__ = "product_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("product_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_seller_reply = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)

    question = relationship("ProductQuestion", back_populates="answers")
    user = relationship("User")


class ReviewHelpfulnessVote(Base, TimestampMixin):
    __tablename__ = "review_helpfulness_votes"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_helpful = Column(Boolean, nullable=False, default=True)

    review = relationship("Review")
    user = relationship("User")


class UserRecentlyViewed(Base):
    __tablename__ = "user_recently_viewed"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    product = relationship("Product")


class PriceAlert(Base, TimestampMixin):
    __tablename__ = "price_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    target_price = Column(Float, nullable=False)
    alert_type = Column(String(50), default="PRICE_DROP")  # PRICE_DROP, BACK_IN_STOCK
    is_triggered = Column(Boolean, default=False)

    user = relationship("User")
    product = relationship("Product")


class InventoryLedger(Base, TimestampMixin):
    __tablename__ = "inventory_ledger"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="SET NULL"), nullable=True)
    transaction_type = Column(String(50), nullable=False)  # INWARD, RESERVATION, DISPATCH, RETURN, ADJUSTMENT
    quantity_change = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    reference_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    product = relationship("Product")


class SellerPayout(Base, TimestampMixin):
    __tablename__ = "seller_payouts"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    commission_deducted = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    status = Column(String(50), default="PROCESSED")  # PENDING, PROCESSED, FAILED
    payout_reference = Column(String(100), unique=True, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    seller = relationship("Seller")
