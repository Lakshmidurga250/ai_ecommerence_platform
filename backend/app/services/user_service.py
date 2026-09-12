"""
User Management and Profile Service.
Handles profile updates, address books, and customer preference management.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException
from app.models.user import User, UserProfile, Address
from app.schemas.user import UserProfileUpdate, AddressCreate, AddressUpdate


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    @staticmethod
    def update_profile(db: Session, user_id: int, data: UserProfileUpdate) -> UserProfile:
        user = UserService.get_user_by_id(db, user_id)
        profile = user.profile
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)

        if data.first_name is not None:
            profile.first_name = data.first_name
        if data.last_name is not None:
            profile.last_name = data.last_name
        if data.phone is not None:
            profile.phone = data.phone
        if data.avatar_url is not None:
            profile.avatar_url = data.avatar_url
        if data.preferences is not None:
            profile.preferences = data.preferences

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def add_address(db: Session, user_id: int, data: AddressCreate) -> Address:
        # If this is the default address, clear default flag from other addresses
        if data.is_default:
            db.query(Address).filter(Address.user_id == user_id).update({"is_default": False})

        address = Address(
            user_id=user_id,
            title=data.title,
            recipient_name=data.recipient_name,
            street=data.street,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country=data.country,
            phone=data.phone,
            is_default=data.is_default
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def list_addresses(db: Session, user_id: int) -> List[Address]:
        return db.query(Address).filter(Address.user_id == user_id).order_by(Address.is_default.desc()).all()

    @staticmethod
    def delete_address(db: Session, user_id: int, address_id: int):
        address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
        if not address:
            raise NotFoundException("Address", str(address_id))
        db.delete(address)
        db.commit()
