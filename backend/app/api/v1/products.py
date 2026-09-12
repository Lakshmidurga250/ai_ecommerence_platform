"""
Product Catalog API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.services.seller_service import SellerService

router = APIRouter(prefix="/products", tags=["Product Catalog"])


@router.get("/", response_model=List[ProductRead])
def list_products(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    category: Optional[str] = Query(None, description="Filter by category slug or name"),
    brand_id: Optional[int] = Query(None, description="Filter by brand ID"),
    brand: Optional[str] = Query(None, description="Filter by brand slug or name"),
    seller_id: Optional[int] = Query(None, description="Filter by seller ID"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum customer rating"),
    in_stock: Optional[bool] = Query(None, description="Filter only in-stock items (alias for in_stock_only)"),
    in_stock_only: bool = Query(False, description="Exclude out-of-stock items"),
    sort: Optional[str] = Query(None, description="Sorting parameter alias for sort_by"),
    sort_by: str = Query("featured", description="Sorting: featured, price_asc, price_desc, rating, popular, newest, discount_desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=250),
    db: Session = Depends(get_db)
):
    """Retrieve filtered, sorted, and paginated products."""
    effective_sort = sort or sort_by
    effective_in_stock = in_stock if in_stock is not None else in_stock_only

    products, _ = ProductService.list_products(
        db=db,
        category_id=category_id,
        category_slug=category,
        brand_id=brand_id,
        brand_slug=brand,
        seller_id=seller_id,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock_only=effective_in_stock,
        sort_by=effective_sort,
        skip=skip,
        limit=limit
    )
    return products



@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve product details by unique product ID."""
    return ProductService.get_product_by_id(db, product_id)


@router.get("/slug/{slug}", response_model=ProductRead)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    """Retrieve product details by SEO slug."""
    return ProductService.get_product_by_slug(db, slug)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Create a new product listing (Authorized Sellers & Admins)."""
    seller = SellerService.get_seller_by_user_id(db, current_user.id)
    return ProductService.create_product(db, seller.id, data)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Update an existing product listing."""
    is_admin = "ADMIN" in current_user.role_names
    seller_id = None if is_admin else SellerService.get_seller_by_user_id(db, current_user.id).id
    return ProductService.update_product(db, product_id, seller_id, data, is_admin=is_admin)
