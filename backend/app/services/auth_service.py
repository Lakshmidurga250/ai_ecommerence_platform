"""
Authentication & User Account Service.
Handles registration, secure login, password hashing, and token generation.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import AuthenticationException, ConflictException, NotFoundException
from app.models.user import User, Role, UserRole, UserProfile
from app.models.cart import Cart, Wishlist
from app.models.audit import AuditLog
from app.schemas.auth import UserRegister, Token


class AuthService:
    @staticmethod
    def register_user(db: Session, data: UserRegister) -> User:
        """Register a new user, assign default role, create profile, and initialize cart/wishlist."""
        # Check existing email
        if db.query(User).filter(User.email == data.email.lower()).first():
            raise ConflictException(f"User with email '{data.email}' already exists")

        # Check existing username
        if db.query(User).filter(User.username == data.username.lower()).first():
            raise ConflictException(f"Username '{data.username}' is already taken")

        # Create user
        user = User(
            email=data.email.lower(),
            username=data.username.lower(),
            hashed_password=hash_password(data.password),
            is_active=True,
            is_verified=True
        )
        db.add(user)
        db.flush()

        # Find or create role
        role = db.query(Role).filter(Role.name == data.role).first()
        if not role:
            role = Role(name=data.role, description=f"{data.role.capitalize()} role")
            db.add(role)
            db.flush()

        user_role = UserRole(user_id=user.id, role_id=role.id)
        db.add(user_role)

        # Create profile
        profile = UserProfile(
            user_id=user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            preferences={}
        )
        db.add(profile)

        # Initialize Cart and Wishlist
        cart = Cart(user_id=user.id)
        wishlist = Wishlist(user_id=user.id)
        db.add(cart)
        db.add(wishlist)

        # Log registration
        audit = AuditLog(
            user_id=user.id,
            action="USER_REGISTER",
            resource_type="user",
            resource_id=str(user.id),
            status="SUCCESS",
            details={"email": user.email, "role": data.role}
        )
        db.add(audit)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email_or_username: str, password: str) -> Token:
        """Authenticate credentials and generate access/refresh JWT tokens."""
        query = email_or_username.lower().strip()
        user = db.query(User).filter((User.email == query) | (User.username == query)).first()

        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Invalid email/username or password")

        if not user.is_active:
            raise AuthenticationException("User account is inactive. Please contact support.")

        roles = user.role_names
        token_payload = {
            "sub": str(user.id),
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "roles": roles
        }

        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        # Log login
        audit = AuditLog(
            user_id=user.id,
            action="USER_LOGIN",
            resource_type="auth",
            resource_id=str(user.id),
            status="SUCCESS",
            details={"email": user.email}
        )
        db.add(audit)
        db.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=3600
        )

    @staticmethod
    def refresh_access_token(db: Session, refresh_token_str: str) -> Token:
        """Issue a new access token from a valid refresh token."""
        payload = decode_token(refresh_token_str)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationException("Invalid or expired refresh token")

        user_id = payload.get("user_id") or payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise AuthenticationException("User account is no longer active")

        token_payload = {
            "sub": str(user.id),
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "roles": user.role_names
        }

        access_token = create_access_token(token_payload)
        new_refresh_token = create_refresh_token(token_payload)

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=3600
        )
