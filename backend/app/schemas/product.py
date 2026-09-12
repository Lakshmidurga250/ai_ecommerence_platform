"""
Product, Category, Brand, and Variant Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    website: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductImageRead(BaseModel):
    id: int
    image_url: str
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False

    model_config = ConfigDict(from_attributes=True)


class ProductVariantRead(BaseModel):
    id: int
    sku: str
    title: str
    price: float
    stock: int
    attributes: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    category_id: int
    brand_id: Optional[int] = None
    sku: str
    name: str
    short_description: Optional[str] = None
    description: str
    price: float = Field(..., gt=0)
    compare_at_price: Optional[float] = None
    cost_price: Optional[float] = None
    discount_percent: float = 0.0
    tax_rate: float = 0.18
    stock: int = Field(default=0, ge=0)
    is_featured: bool = False
    attributes: Dict[str, Any] = {}
    images: List[str] = []  # List of image URLs


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    name: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    compare_at_price: Optional[float] = None
    cost_price: Optional[float] = None
    discount_percent: Optional[float] = None
    tax_rate: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    attributes: Optional[Dict[str, Any]] = None


class ProductRead(BaseModel):
    id: int
    seller_id: int
    category_id: int
    brand_id: Optional[int] = None
    sku: str
    name: str
    slug: str
    short_description: Optional[str] = None
    description: str
    price: float
    compare_at_price: Optional[float] = None
    discount_percent: float
    tax_rate: float
    stock: int
    is_active: bool
    is_featured: bool
    rating: float
    review_count: int
    sales_count: int
    attributes: Dict[str, Any] = {}
    category: Optional[CategoryRead] = None
    brand: Optional[BrandRead] = None
    images: List[ProductImageRead] = []
    variants: List[ProductVariantRead] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
