"""
Product Catalog, Category, and Brand Management Service.
"""

import re
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.core.exceptions import NotFoundException, ConflictException, AuthorizationException
from app.models.product import Product, Category, Brand, ProductImage, ProductVariant
from app.models.inventory import Warehouse, Inventory, InventoryMovement
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate, BrandCreate


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text)


class ProductService:
    @staticmethod
    def create_category(db: Session, data: CategoryCreate) -> Category:
        existing = db.query(Category).filter((Category.name == data.name) | (Category.slug == data.slug)).first()
        if existing:
            raise ConflictException(f"Category '{data.name}' already exists")
        cat = Category(
            name=data.name,
            slug=data.slug,
            description=data.description,
            image_url=data.image_url,
            parent_id=data.parent_id
        )
        db.add(cat)
        db.commit()
        db.refresh(cat)
        return cat

    @staticmethod
    def list_categories(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def create_brand(db: Session, data: BrandCreate) -> Brand:
        existing = db.query(Brand).filter((Brand.name == data.name) | (Brand.slug == data.slug)).first()
        if existing:
            raise ConflictException(f"Brand '{data.name}' already exists")
        brand = Brand(
            name=data.name,
            slug=data.slug,
            logo_url=data.logo_url,
            website=data.website
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand

    @staticmethod
    def list_brands(db: Session) -> List[Brand]:
        return db.query(Brand).all()

    @staticmethod
    def create_product(db: Session, seller_id: int, data: ProductCreate) -> Product:
        # Check SKU uniqueness
        if db.query(Product).filter(Product.sku == data.sku).first():
            raise ConflictException(f"Product SKU '{data.sku}' already exists")

        base_slug = slugify(data.name)
        slug = base_slug
        counter = 1
        while db.query(Product).filter(Product.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product(
            seller_id=seller_id,
            category_id=data.category_id,
            brand_id=data.brand_id,
            sku=data.sku,
            name=data.name,
            slug=slug,
            short_description=data.short_description,
            description=data.description,
            price=data.price,
            compare_at_price=data.compare_at_price,
            cost_price=data.cost_price,
            discount_percent=data.discount_percent,
            tax_rate=data.tax_rate,
            stock=data.stock,
            is_active=True,
            is_featured=data.is_featured,
            attributes=data.attributes
        )
        db.add(product)
        db.flush()

        # Add images
        for idx, img_url in enumerate(data.images):
            image = ProductImage(
                product_id=product.id,
                image_url=img_url,
                sort_order=idx,
                is_primary=(idx == 0)
            )
            db.add(image)

        # Allocate default warehouse inventory if warehouse exists
        warehouse = db.query(Warehouse).first()
        if not warehouse:
            warehouse = Warehouse(
                name="Central Fulfillment Hub",
                code="WH-CENTRAL-01",
                address="100 Tech Park Way",
                city="Bengaluru",
                state="Karnataka",
                postal_code="560100",
                country="India",
                capacity_units=100000
            )
            db.add(warehouse)
            db.flush()

        inventory = Inventory(
            warehouse_id=warehouse.id,
            product_id=product.id,
            quantity=data.stock,
            reserved_quantity=0,
            reorder_level=10
        )
        db.add(inventory)
        db.flush()

        if data.stock > 0:
            movement = InventoryMovement(
                inventory_id=inventory.id,
                movement_type="INBOUND",
                quantity=data.stock,
                reference_type="INITIAL_STOCK",
                reference_id=product.sku,
                notes="Initial product catalog onboarding"
            )
            db.add(movement)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundException("Product", str(product_id))
        return product

    @staticmethod
    def get_product_by_slug(db: Session, slug: str) -> Product:
        product = db.query(Product).filter(Product.slug == slug).first()
        if not product:
            raise NotFoundException("Product", slug)
        return product

    @staticmethod
    def update_product(db: Session, product_id: int, seller_id: Optional[int], data: ProductUpdate, is_admin: bool = False) -> Product:
        product = ProductService.get_product_by_id(db, product_id)
        if not is_admin and product.seller_id != seller_id:
            raise AuthorizationException("You are not authorized to modify products belonging to another seller")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def list_products(
        db: Session,
        category_id: Optional[int] = None,
        brand_id: Optional[int] = None,
        seller_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        in_stock_only: bool = False,
        sort_by: str = "featured",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Product], int]:
        query = db.query(Product).filter(Product.is_active == True)

        if category_id:
            query = query.filter(Product.category_id == category_id)
        if brand_id:
            query = query.filter(Product.brand_id == brand_id)
        if seller_id:
            query = query.filter(Product.seller_id == seller_id)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if min_rating is not None:
            query = query.filter(Product.rating >= min_rating)
        if in_stock_only:
            query = query.filter(Product.stock > 0)

        total = query.count()

        if sort_by == "price_asc":
            query = query.order_by(asc(Product.price))
        elif sort_by == "price_desc":
            query = query.order_by(desc(Product.price))
        elif sort_by == "rating":
            query = query.order_by(desc(Product.rating))
        elif sort_by == "popular":
            query = query.order_by(desc(Product.sales_count))
        elif sort_by == "newest":
            query = query.order_by(desc(Product.created_at))
        else:
            query = query.order_by(desc(Product.is_featured), desc(Product.rating))

        products = query.offset(skip).limit(limit).all()
        return products, total
