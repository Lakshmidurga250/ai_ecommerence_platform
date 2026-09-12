"""
Authentication API Endpoints: Register, Login, Refresh, and Profile.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import UserRegister, UserLogin, RefreshTokenRequest, Token
from app.schemas.user import UserRead
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account (Customer, Seller, or Admin)."""
    user = AuthService.register_user(db, data)
    return user


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with email/username and password to receive JWT access and refresh tokens."""
    return AuthService.authenticate_user(db, data.email_or_username, data.password)


@router.post("/refresh", response_model=Token)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Generate a new access token using a valid refresh token."""
    return AuthService.refresh_access_token(db, data.refresh_token)


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get authenticated user's account details and roles."""
    return current_user
