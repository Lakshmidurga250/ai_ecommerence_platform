"""
User Management and Address Book API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserProfileRead, UserProfileUpdate, AddressCreate, AddressRead, AddressUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/profile", response_model=UserProfileRead)
def get_profile(current_user: User = Depends(get_current_user)):
    """Retrieve current user's profile information."""
    return current_user.profile or UserProfileRead()


@router.put("/profile", response_model=UserProfileRead)
def update_profile(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update profile details (name, phone, avatar, preferences)."""
    return UserService.update_profile(db, current_user.id, data)


@router.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all saved shipping addresses for current customer."""
    return UserService.list_addresses(db, current_user.id)


@router.post("/addresses", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new delivery address."""
    return UserService.add_address(db, current_user.id, data)


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove an address from the address book."""
    UserService.delete_address(db, current_user.id, address_id)
