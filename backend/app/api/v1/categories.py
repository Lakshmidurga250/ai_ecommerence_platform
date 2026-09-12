"""
Categories and Brands Taxonomy API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from app.models.user import User
from app.schemas.product import CategoryRead, CategoryCreate, BrandRead, BrandCreate
from app.services.product_service import ProductService

router = APIRouter(prefix="/categories", tags=["Taxonomy"])


@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    """List all available marketplace categories."""
    return ProductService.list_categories(db)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Create a new marketplace category (Admins only)."""
    return ProductService.create_category(db, data)


@router.get("/brands", response_model=List[BrandRead])
def list_brands(db: Session = Depends(get_db)):
    """List all available brands."""
    return ProductService.list_brands(db)


@router.post("/brands", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
def create_brand(
    data: BrandCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Create a new brand (Admins only)."""
    return ProductService.create_brand(db, data)
