"""
Seller Management Service for Multi-Vendor Marketplace.
Handles seller onboarding, storefront profiles, and seller isolation.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException, AuthorizationException
from app.models.seller import Seller, SellerProfile, SellerStatus
from app.models.user import User, Role, UserRole
from app.schemas.seller import SellerRegister, SellerUpdate, SellerProfileUpdate


class SellerService:
    @staticmethod
    def register_seller(db: Session, user: User, data: SellerRegister) -> Seller:
        # Verify user is not already a seller
        existing = db.query(Seller).filter(Seller.user_id == user.id).first()
        if existing:
            raise ConflictException("You already have an existing seller account")

        # Check unique store name
        if db.query(Seller).filter(Seller.store_name == data.store_name).first():
            raise ConflictException(f"Store name '{data.store_name}' is already taken")

        # Create Seller record
        seller = Seller(
            user_id=user.id,
            store_name=data.store_name,
            legal_name=data.legal_name,
            business_email=data.business_email,
            business_phone=data.business_phone,
            tax_identifier=data.tax_identifier,
            status=SellerStatus.APPROVED.value,  # Auto-approve in dev/standalone mode
            rating=5.0,
            total_sales_count=0,
            commission_rate=0.10
        )
        db.add(seller)
        db.flush()

        # Add profile
        profile = SellerProfile(
            seller_id=seller.id,
            description=data.description,
            support_email=data.business_email
        )
        db.add(profile)

        # Grant SELLER role to user if not already assigned
        seller_role = db.query(Role).filter(Role.name == "SELLER").first()
        if seller_role:
            has_role = db.query(UserRole).filter(UserRole.user_id == user.id, UserRole.role_id == seller_role.id).first()
            if not has_role:
                db.add(UserRole(user_id=user.id, role_id=seller_role.id))

        db.commit()
        db.refresh(seller)
        return seller

    @staticmethod
    def get_seller_by_user_id(db: Session, user_id: int) -> Seller:
        seller = db.query(Seller).filter(Seller.user_id == user_id).first()
        if not seller:
            raise NotFoundException("Seller account for current user not found")
        return seller

    @staticmethod
    def get_seller_by_id(db: Session, seller_id: int) -> Seller:
        seller = db.query(Seller).filter(Seller.id == seller_id).first()
        if not seller:
            raise NotFoundException("Seller", str(seller_id))
        return seller

    @staticmethod
    def update_seller_profile(db: Session, seller_id: int, data: SellerProfileUpdate) -> SellerProfile:
        seller = SellerService.get_seller_by_id(db, seller_id)
        profile = seller.profile
        if not profile:
            profile = SellerProfile(seller_id=seller_id)
            db.add(profile)

        if data.logo_url is not None:
            profile.logo_url = data.logo_url
        if data.banner_url is not None:
            profile.banner_url = data.banner_url
        if data.description is not None:
            profile.description = data.description
        if data.support_email is not None:
            profile.support_email = data.support_email
        if data.return_policy is not None:
            profile.return_policy = data.return_policy
        if data.shipping_policy is not None:
            profile.shipping_policy = data.shipping_policy

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update_seller_status(db: Session, seller_id: int, new_status: str) -> Seller:
        seller = SellerService.get_seller_by_id(db, seller_id)
        seller.status = new_status
        db.commit()
        db.refresh(seller)
        return seller

    @staticmethod
    def list_sellers(db: Session, skip: int = 0, limit: int = 50) -> List[Seller]:
        return db.query(Seller).offset(skip).limit(limit).all()
