"""
Customer Loyalty & Rewards Engine.
Manages points accrual, tier progression (BRONZE to DIAMOND), and coupon reward redemptions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.platform_expansion_v2 import LoyaltyAccount, LoyaltyTransaction
from app.models.cart import Coupon
from app.models.user import User


class LoyaltyService:
    """
    Manages customer loyalty accounts, reward points ledger, and tier advancements.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def get_loyalty_profile(self, user_id: int) -> Dict[str, Any]:
        if not self.db:
            return {"user_id": user_id, "tier": "BRONZE", "current_points": 100, "points_balance": 100, "lifetime_points": 100, "lifetime_spend": 0.0}
        return self.get_loyalty_summary(self.db, user_id)

    TIERS = [
        ("DIAMOND", 10000, 0.15),  # 15% VIP perks
        ("PLATINUM", 5000, 0.10),
        ("GOLD", 1500, 0.05),
        ("SILVER", 500, 0.02),
        ("BRONZE", 0, 0.0)
    ]

    @classmethod
    def get_or_create_account(cls, db: Session, user_id: int) -> LoyaltyAccount:
        """
        Retrieves or initializes a customer's loyalty account.
        """
        account = db.query(LoyaltyAccount).filter(LoyaltyAccount.user_id == user_id).first()
        if not account:
            account = LoyaltyAccount(
                user_id=user_id,
                points_balance=100,  # 100 welcome bonus points
                tier="BRONZE",
                lifetime_points=100,
                lifetime_spend=0.0
            )
            db.add(account)
            db.flush()

            # Record welcome transaction
            db.add(LoyaltyTransaction(
                loyalty_account_id=account.id,
                points_delta=100,
                transaction_type="WELCOME_BONUS",
                notes="Welcome bonus points upon registration"
            ))
            db.commit()
            db.refresh(account)

        return account

    @classmethod
    def accrue_order_points(cls, db: Session, user_id: int, order_id: int, order_amount: float) -> LoyaltyAccount:
        """
        Awards 1 point per ₹100 spent and updates tier.
        """
        account = cls.get_or_create_account(db, user_id)
        earned_points = max(1, int(order_amount // 100))

        account.points_balance += earned_points
        account.lifetime_points += earned_points
        account.lifetime_spend += order_amount

        # Update tier
        for tier_name, min_pts, _ in cls.TIERS:
            if account.lifetime_points >= min_pts:
                account.tier = tier_name
                break

        db.add(LoyaltyTransaction(
            loyalty_account_id=account.id,
            points_delta=earned_points,
            transaction_type="PURCHASE_EARN",
            order_id=order_id,
            notes=f"Earned from order (₹{order_amount:,.2f})"
        ))
        db.commit()
        db.refresh(account)
        return account

    @classmethod
    def redeem_points_for_coupon(cls, db: Session, user_id: int, points_to_redeem: int) -> Dict[str, Any]:
        """
        Redeems points for an instant discount coupon (e.g., 200 points = ₹100 off).
        """
        account = cls.get_or_create_account(db, user_id)
        if points_to_redeem <= 0 or points_to_redeem > account.points_balance:
            from app.core.exceptions import BadRequestException
            raise BadRequestException(f"Insufficient points balance ({account.points_balance} available).")

        discount_rupees = round(points_to_redeem * 0.5, 2)  # 2 points = ₹1
        coupon_code = f"REWARD-{user_id}-{int(discount_rupees)}"

        # Check or create coupon
        coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
        if not coupon:
            coupon = Coupon(
                code=coupon_code,
                discount_type="FIXED",
                discount_value=discount_rupees,
                min_order_amount=discount_rupees * 2.0,
                max_discount_amount=discount_rupees,
                valid_from=datetime.now(timezone.utc),
                valid_until=datetime.now(timezone.utc) + timedelta(days=60),
                usage_limit=1,
                is_active=True
            )
            db.add(coupon)
            db.flush()

        account.points_balance -= points_to_redeem
        db.add(LoyaltyTransaction(
            loyalty_account_id=account.id,
            points_delta=-points_to_redeem,
            transaction_type="REWARD_REDEMPTION",
            notes=f"Redeemed for ₹{discount_rupees} coupon ({coupon_code})"
        ))

        db.commit()
        db.refresh(account)

        return {
            "coupon_code": coupon_code,
            "discount_value": discount_rupees,
            "points_redeemed": points_to_redeem,
            "remaining_points": account.points_balance,
            "valid_until": coupon.valid_until.isoformat()
        }

    @classmethod
    def get_loyalty_summary(cls, db: Session, user_id: int) -> Dict[str, Any]:
        """
        Returns full loyalty profile with points, tier perks, and redemption options.
        """
        account = cls.get_or_create_account(db, user_id)
        txns = db.query(LoyaltyTransaction).filter(
            LoyaltyTransaction.loyalty_account_id == account.id
        ).order_by(desc(LoyaltyTransaction.created_at)).limit(10).all()

        return {
            "account_id": account.id,
            "user_id": account.user_id,
            "tier": account.tier,
            "current_points": account.points_balance,
            "points_balance": account.points_balance,
            "lifetime_points": account.lifetime_points,
            "lifetime_spend": round(account.lifetime_spend, 2),
            "points_expiring_soon": 0,
            "tier_perks": [
                f"{account.tier} Tier Verified",
                "Earn 1 Point per ₹100 on all orders",
                "Birthday Surprise Bonus",
                "Exclusive Early Access to Seasonal Sales"
            ],
            "redemption_options": [
                {"points": 200, "discount": 100.0, "label": "₹100 Off Coupon"},
                {"points": 500, "discount": 250.0, "label": "₹250 Off Coupon"},
                {"points": 1000, "discount": 500.0, "label": "₹500 Off Coupon"}
            ],
            "recent_transactions": [{
                "id": t.id,
                "points": t.points_delta,
                "points_delta": t.points_delta,
                "transaction_type": t.transaction_type,
                "type": t.transaction_type,
                "description": t.notes or "",
                "notes": t.notes or "",
                "created_at": t.created_at.isoformat() if t.created_at else None
            } for t in txns]
        }
