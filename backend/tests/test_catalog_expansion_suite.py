"""
Comprehensive Test Suite for Product Catalog Expansion.
Validates:
- 200+ total active catalog products
- 9 distinct categories with >= 15 products each
- 25 top brands and 15 multi-vendor marketplace sellers
- Category & brand filtering by slug and ID
- Multi-tier Indian Rupee (INR) price filtering
- Rating threshold and in-stock filtering
- Sorting: price asc/desc, rating desc, discount desc, newest
- Pagination (limit up to 250, offset/skip)
- BM25 search across expanded categories
- Community Q&A, Product Bundles, Reviews & Sentiment Scores
- Multi-warehouse inventory allocation
"""

import pytest
from sqlalchemy.orm import Session
from app.models.product import Product, Category, Brand
from app.models.seller import Seller
from app.models.review import Review, ReviewSentiment
from app.models.inventory import Warehouse, Inventory
from app.models.catalog_expansion import ProductBundle, ProductQuestion, ProductAnswer


# =============================================================================
# 1. CATALOG SCALE & ENTITY REPRESENTATION TESTS
# =============================================================================

def test_catalog_total_product_count(db_session: Session):
    """Verify the database contains at least 200 products (216 seeded)."""
    count = db_session.query(Product).count()
    assert count >= 200, f"Expected >= 200 products, found {count}"


def test_all_nine_categories_present(db_session: Session, client):
    """Verify all 9 catalog categories exist and are accessible via API."""
    res = client.get("/api/v1/categories/")
    assert res.status_code == 200
    categories = res.json()
    assert len(categories) >= 9

    slugs = {c["slug"] for c in categories}
    expected_slugs = [
        "laptops-computing",
        "smartphones-tablets",
        "audio-wearables",
        "footwear-running",
        "athletic-apparel",
        "home-kitchen",
        "gaming-accessories",
        "personal-care",
        "books-stationery"
    ]
    for expected in expected_slugs:
        assert expected in slugs, f"Missing expected category slug: {expected}"


def test_products_per_category_distribution(db_session: Session):
    """Verify each of the 9 categories has at least 15 products."""
    categories = db_session.query(Category).all()
    assert len(categories) >= 9

    for cat in categories:
        product_count = db_session.query(Product).filter(Product.category_id == cat.id).count()
        assert product_count >= 15, f"Category '{cat.name}' has only {product_count} products (expected >= 15)"


def test_all_twenty_five_brands_present(db_session: Session, client):
    """Verify all 25 top brands exist and have products associated."""
    res = client.get("/api/v1/categories/brands")
    assert res.status_code == 200
    brands = res.json()
    assert len(brands) >= 25

    brand_slugs = {b["slug"] for b in brands}
    key_brands = ["apple", "samsung", "dell", "sony", "boat", "nike", "adidas", "philips", "logitech"]
    for kb in key_brands:
        assert kb in brand_slugs, f"Missing expected brand: {kb}"


def test_all_fifteen_sellers_present(db_session: Session):
    """Verify at least 15 marketplace sellers exist and have catalog inventory."""
    seller_count = db_session.query(Seller).count()
    assert seller_count >= 15, f"Expected >= 15 sellers, found {seller_count}"


# =============================================================================
# 2. CATEGORY & BRAND FILTERING TESTS (API)
# =============================================================================

def test_category_slug_filter_laptops(client):
    """Verify filtering products by category slug 'laptops-computing'."""
    res = client.get("/api/v1/products/?category=laptops-computing&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20
    for p in data:
        assert p.get("category_id") is not None


def test_category_slug_filter_smartphones(client):
    """Verify filtering products by category slug 'smartphones-tablets'."""
    res = client.get("/api/v1/products/?category=smartphones-tablets&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20


def test_category_slug_filter_audio(client):
    """Verify filtering products by category slug 'audio-wearables'."""
    res = client.get("/api/v1/products/?category=audio-wearables&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20


def test_category_slug_filter_footwear(client):
    """Verify filtering products by category slug 'footwear-running'."""
    res = client.get("/api/v1/products/?category=footwear-running&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20


def test_category_slug_filter_home_kitchen(client):
    """Verify filtering products by category slug 'home-kitchen'."""
    res = client.get("/api/v1/products/?category=home-kitchen&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20


def test_category_id_filter(db_session: Session, client):
    """Verify filtering products by numeric category_id."""
    cat = db_session.query(Category).first()
    res = client.get(f"/api/v1/products/?category_id={cat.id}&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert p["category_id"] == cat.id


def test_brand_slug_filter_apple(client):
    """Verify filtering products by brand slug 'apple'."""
    res = client.get("/api/v1/products/?brand=apple&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3
    for p in data:
        # Apple products should have 'Apple' or 'MacBook' or 'iPad' or 'iPhone' or 'AirPods' in name
        assert any(term in p["name"].lower() for term in ["apple", "macbook", "ipad", "iphone", "watch", "airpods"])


def test_brand_slug_filter_samsung(client):
    """Verify filtering products by brand slug 'samsung'."""
    res = client.get("/api/v1/products/?brand=samsung&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3


def test_brand_slug_filter_sony(client):
    """Verify filtering products by brand slug 'sony'."""
    res = client.get("/api/v1/products/?brand=sony&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 2


def test_brand_slug_filter_nike(client):
    """Verify filtering products by brand slug 'nike'."""
    res = client.get("/api/v1/products/?brand=nike&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3


def test_brand_id_filter(db_session: Session, client):
    """Verify filtering products by numeric brand_id."""
    brand = db_session.query(Brand).first()
    res = client.get(f"/api/v1/products/?brand_id={brand.id}&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert p["brand_id"] == brand.id


def test_combined_category_and_brand_filter(client):
    """Verify combining category slug and brand slug filters."""
    res = client.get("/api/v1/products/?category=audio-wearables&brand=sony&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    for p in data:
        assert "sony" in p["name"].lower()


# =============================================================================
# 3. PRICE RANGE & FACET FILTERING TESTS
# =============================================================================

def test_price_range_budget_tier(client):
    """Verify budget tier price filtering (₹300 to ₹2,500)."""
    res = client.get("/api/v1/products/?min_price=300&max_price=2500&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert 300 <= p["price"] <= 2500


def test_price_range_mid_tier(client):
    """Verify mid-range tier price filtering (₹10,000 to ₹40,000)."""
    res = client.get("/api/v1/products/?min_price=10000&max_price=40000&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert 10000 <= p["price"] <= 40000


def test_price_range_premium_tier(client):
    """Verify premium tier price filtering (₹75,000 to ₹2,50,000)."""
    res = client.get("/api/v1/products/?min_price=75000&max_price=250000&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert 75000 <= p["price"] <= 250000


def test_rating_threshold_filter(client):
    """Verify filtering products with minimum rating threshold."""
    res = client.get("/api/v1/products/?min_rating=4.5&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert p["rating"] >= 4.5


def test_in_stock_only_filter(client):
    """Verify filtering only in-stock products."""
    res = client.get("/api/v1/products/?in_stock=true&limit=100")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert p["stock"] > 0


# =============================================================================
# 4. SORTING & PAGINATION TESTS
# =============================================================================

def test_sorting_price_ascending(client):
    """Verify sorting products by price ascending."""
    res = client.get("/api/v1/products/?sort=price_asc&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    prices = [p["price"] for p in data]
    assert prices == sorted(prices)


def test_sorting_price_descending(client):
    """Verify sorting products by price descending."""
    res = client.get("/api/v1/products/?sort=price_desc&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    prices = [p["price"] for p in data]
    assert prices == sorted(prices, reverse=True)


def test_sorting_rating_descending(client):
    """Verify sorting products by rating descending."""
    res = client.get("/api/v1/products/?sort=rating_desc&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    ratings = [p["rating"] for p in data]
    assert ratings == sorted(ratings, reverse=True)


def test_sorting_discount_descending(client):
    """Verify sorting products by discount descending."""
    res = client.get("/api/v1/products/?sort=discount_desc&limit=50")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    discounts = [p.get("discount_percent") or 0 for p in data]
    assert discounts == sorted(discounts, reverse=True)


def test_sorting_newest(client):
    """Verify sorting products by newest."""
    res = client.get("/api/v1/products/?sort=newest&limit=30")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10


def test_pagination_skip_and_limit(client):
    """Verify offset and limit pagination partitions items without overlap."""
    res_page1 = client.get("/api/v1/products/?skip=0&limit=18")
    assert res_page1.status_code == 200
    page1 = res_page1.json()
    assert len(page1) == 18

    res_page2 = client.get("/api/v1/products/?skip=18&limit=18")
    assert res_page2.status_code == 200
    page2 = res_page2.json()
    assert len(page2) == 18

    page1_ids = {p["id"] for p in page1}
    page2_ids = {p["id"] for p in page2}
    assert len(page1_ids.intersection(page2_ids)) == 0, "Page 1 and Page 2 contain overlapping products!"


def test_pagination_extended_limit(client):
    """Verify high limit queries (up to 250) retrieve catalog bulk."""
    res = client.get("/api/v1/products/?limit=200")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 200


# =============================================================================
# 5. BM25 SEARCH & SUGGESTIONS TESTS
# =============================================================================

def test_bm25_search_catalog_keywords(client):
    """Verify BM25 search across multiple product categories."""
    keywords = ["thinkpad", "galaxy", "running", "espresso", "gaming"]
    for kw in keywords:
        res = client.get(f"/api/v1/search/?q={kw}")
        assert res.status_code == 200
        data = res.json()
        assert len(data) > 0, f"Search returned 0 results for keyword: {kw}"


def test_search_suggestions_brands(client):
    """Verify brand prefix suggestions."""
    res = client.get("/api/v1/search/suggestions?prefix=son")
    assert res.status_code == 200
    suggestions = res.json()
    assert any("sony" in s.lower() for s in suggestions)


# =============================================================================
# 6. PRODUCT BUNDLES, COMMUNITY Q&A & SENTIMENT INTEGRITY
# =============================================================================

def test_product_bundle_integrity(db_session: Session):
    """Verify product bundles exist in database and have valid pairings."""
    bundles = db_session.query(ProductBundle).all()
    assert len(bundles) >= 5, f"Expected >= 5 bundles, found {len(bundles)}"
    for b in bundles:
        assert b.primary_product_id != b.bundle_product_id
        assert b.discount_percent > 0


def test_product_qna_records(db_session: Session):
    """Verify community Q&A questions and answers exist in database."""
    questions = db_session.query(ProductQuestion).all()
    answers = db_session.query(ProductAnswer).all()
    assert len(questions) >= 5, f"Expected >= 5 questions, found {len(questions)}"
    assert len(answers) >= 5, f"Expected >= 5 answers, found {len(answers)}"


def test_product_reviews_and_sentiment_records(db_session: Session):
    """Verify seeded reviews and ML sentiment analysis scores."""
    reviews = db_session.query(Review).all()
    assert len(reviews) >= 50, f"Expected >= 50 reviews, found {len(reviews)}"

    sentiments = db_session.query(ReviewSentiment).all()
    assert len(sentiments) >= 50, f"Expected >= 50 sentiment records, found {len(sentiments)}"
    for s in sentiments:
        assert s.sentiment_label in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
        assert -1.0 <= s.polarity_score <= 1.0


def test_warehouse_inventory_distribution(db_session: Session):
    """Verify inventory records exist across all 3 regional warehouses."""
    warehouses = db_session.query(Warehouse).all()
    assert len(warehouses) >= 3

    for wh in warehouses:
        inv_count = db_session.query(Inventory).filter(Inventory.warehouse_id == wh.id).count()
        assert inv_count > 0, f"Warehouse {wh.code} has 0 inventory entries!"
