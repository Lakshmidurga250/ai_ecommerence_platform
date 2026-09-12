"""
Catalog Metrics Collector Script.
Queries ecommerce.db and outputs complete catalog distribution statistics
for the final audit documentation.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.core.database import SessionLocal
from app.models.product import Product, Category, Brand
from app.models.seller import Seller
from app.models.review import Review, ReviewSentiment
from app.models.catalog_expansion import ProductBundle, ProductQuestion, ProductAnswer
from app.models.inventory import Warehouse, Inventory
from sqlalchemy import func


def collect_metrics():
    db = SessionLocal()
    try:
        total_products = db.query(Product).count()
        active_products = db.query(Product).filter(Product.is_active == True).count()
        featured_products = db.query(Product).filter(Product.is_featured == True).count()

        prices = [p.price for p in db.query(Product.price).all()]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) / len(prices) if prices else 0
        sorted_prices = sorted(prices)
        median_price = sorted_prices[len(sorted_prices) // 2] if sorted_prices else 0

        # Category Breakdown
        categories = db.query(Category).all()
        cat_stats = []
        for c in categories:
            cnt = db.query(Product).filter(Product.category_id == c.id).count()
            cat_stats.append((c.name, c.slug, cnt))

        # Brand Breakdown
        brands = db.query(Brand).all()
        brand_stats = []
        for b in brands:
            cnt = db.query(Product).filter(Product.brand_id == b.id).count()
            brand_stats.append((b.name, b.slug, cnt))

        # Seller Breakdown
        sellers = db.query(Seller).all()
        seller_stats = []
        for s in sellers:
            cnt = db.query(Product).filter(Product.seller_id == s.id).count()
            seller_stats.append((s.store_name, s.user.username if s.user else "unknown", cnt))

        # Review & Sentiment Breakdown
        total_reviews = db.query(Review).count()
        avg_rating = db.query(func.avg(Review.rating)).scalar() or 0.0
        sentiment_records = db.query(ReviewSentiment).count()
        pos_sent = db.query(ReviewSentiment).filter(ReviewSentiment.sentiment_label == "POSITIVE").count()
        neu_sent = db.query(ReviewSentiment).filter(ReviewSentiment.sentiment_label == "NEUTRAL").count()
        neg_sent = db.query(ReviewSentiment).filter(ReviewSentiment.sentiment_label == "NEGATIVE").count()

        # Bundles & Q&A
        bundles_cnt = db.query(ProductBundle).count()
        questions_cnt = db.query(ProductQuestion).count()
        answers_cnt = db.query(ProductAnswer).count()

        # Warehouses & Inventory
        warehouses = db.query(Warehouse).all()
        wh_stats = []
        total_inventory_units = 0
        for w in warehouses:
            units = db.query(func.sum(Inventory.quantity)).filter(Inventory.warehouse_id == w.id).scalar() or 0
            total_inventory_units += units
            wh_stats.append((w.name, w.code, units))

        print("=" * 60)
        print("CATALOG METRICS SUMMARY REPORT")
        print("=" * 60)
        print(f"Total Products: {total_products} (Active: {active_products}, Featured: {featured_products})")
        print(f"Price Metrics: Min = ₹{min_price:,.2f} | Max = ₹{max_price:,.2f} | Avg = ₹{avg_price:,.2f} | Median = ₹{median_price:,.2f}")
        print("-" * 60)
        print(f"Categories ({len(cat_stats)}):")
        for name, slug, cnt in cat_stats:
            print(f"  - {name} ({slug}): {cnt} products")
        print("-" * 60)
        print(f"Brands ({len(brand_stats)}):")
        for name, slug, cnt in brand_stats:
            print(f"  - {name} ({slug}): {cnt} products")
        print("-" * 60)
        print(f"Sellers ({len(seller_stats)}):")
        for sname, uname, cnt in seller_stats:
            print(f"  - {sname} (@{uname}): {cnt} products")
        print("-" * 60)
        print(f"Customer Reviews & Sentiments:")
        print(f"  - Total Reviews: {total_reviews} (Average Rating: {avg_rating:.2f}★)")
        print(f"  - Sentiment Analysis Records: {sentiment_records} (Positive: {pos_sent}, Neutral: {neu_sent}, Negative: {neg_sent})")
        print(f"Bundles & Q&A:")
        print(f"  - Product Bundles: {bundles_cnt}")
        print(f"  - Community Questions: {questions_cnt} | Answers: {answers_cnt}")
        print(f"Warehouses & Stock:")
        print(f"  - Total Stock Units in Network: {total_inventory_units:,}")
        for wname, wcode, units in wh_stats:
            print(f"  - {wname} ({wcode}): {units:,} units")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    collect_metrics()
