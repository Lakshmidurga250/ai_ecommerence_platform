"""
FastAPI Authentication & RBAC Dependencies.
Enforces JWT token extraction and role-based permissions at the backend layer.
"""

from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import AuthenticationException, AuthorizationException
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Extract and validate the current authenticated user from JWT Bearer token."""
    if not token:
        raise AuthenticationException("Authentication token is required")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise AuthenticationException("Invalid or expired authentication token")

    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise AuthenticationException("Malformed authentication token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise AuthenticationException("User account associated with this token not found")

    if not user.is_active:
        raise AuthenticationException("User account has been deactivated")

    return user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Optional user dependency for endpoints that work for both guest and authenticated users."""
    if not token:
        return None
    try:
        return get_current_user(token=token, db=db)
    except AuthenticationException:
        return None


class RoleChecker:
    """Dependency for enforcing Role-Based Access Control (RBAC)."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = set(allowed_roles)

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_roles = set(current_user.role_names)
        # ADMIN has superuser access to all routes
        if "ADMIN" in user_roles:
            return current_user
            
        if not self.allowed_roles.intersection(user_roles):
            raise AuthorizationException(
                f"Action requires one of the following roles: {', '.join(sorted(self.allowed_roles))}"
            )
        return current_user
