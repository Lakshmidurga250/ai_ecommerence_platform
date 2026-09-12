"""
Product Catalog, Category, Brand, Variant, and Attribute Models.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")


class Brand(Base, TimestampMixin):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)

    products = relationship("Product", back_populates="brand")


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="SET NULL"), nullable=True, index=True)
    
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    slug = Column(String(300), unique=True, index=True, nullable=False)
    short_description = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    
    price = Column(Float, nullable=False, index=True)
    compare_at_price = Column(Float, nullable=True)  # Original MSRP
    cost_price = Column(Float, nullable=True)
    discount_percent = Column(Float, default=0.0, nullable=False)
    tax_rate = Column(Float, default=0.18, nullable=False)  # e.g., 18% GST
    
    stock = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    rating = Column(Float, default=0.0, nullable=False, index=True)
    review_count = Column(Integer, default=0, nullable=False)
    sales_count = Column(Integer, default=0, nullable=False, index=True)
    
    attributes = Column(JSON, default=dict, nullable=False)  # e.g., {"color": "black", "size": "M"}

    seller = relationship("Seller", back_populates="products")
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(Base, TimestampMixin):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(150), nullable=False)  # e.g. "Red / XL"
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    attributes = Column(JSON, default=dict, nullable=False)

    product = relationship("Product", back_populates="variants")


class ProductImage(Base, TimestampMixin):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)

    product = relationship("Product", back_populates="images")
