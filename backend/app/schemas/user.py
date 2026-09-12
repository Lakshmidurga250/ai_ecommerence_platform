"""
User, Profile, and Address Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


class AddressBase(BaseModel):
    title: str = "Home"
    recipient_name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "India"
    phone: str
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    title: Optional[str] = None
    recipient_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    is_default: Optional[bool] = None


class AddressRead(AddressBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserProfileRead(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool
    roles: List[str] = []
    profile: Optional[UserProfileRead] = None
    created_at: datetime

    @field_validator("roles", mode="before")
    def extract_roles(cls, v):
        if not v:
            return []
        if isinstance(v, list) and len(v) > 0 and hasattr(v[0], "role"):
            return [ur.role.name for ur in v if hasattr(ur, "role") and ur.role]
        return [str(item) for item in v]

    model_config = ConfigDict(from_attributes=True)
