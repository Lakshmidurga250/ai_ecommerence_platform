"""
Test Suite: AI Outfit & Bundle Intelligence Engine.
Tests multi-partite category compatibility graphs, price proportionality,
dynamic bundle discounts, and tiered bundle synthesis.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.product import Product
from ai.recommendations.outfit_bundle_generator import OutfitBundleGenerator
from ai.recommendations.bundle_recommender import BundleRecommender

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_outfit_generator_footwear_anchor(db_session):
    generator = OutfitBundleGenerator(db_session)
    # Find a footwear product
    prod = db_session.query(Product).join(Product.category).filter(Product.category.has(slug="footwear-running")).first()
    if not prod:
        prod = db_session.query(Product).first()

    outfit = generator.generate_outfit_for_product(product_id=prod.id, bundle_size=3, discount_percentage=12.0)
    assert "error" not in outfit
    assert outfit["focal_product_id"] == prod.id
    assert outfit["items_count"] >= 2
    assert outfit["bundle_discount_pct"] == 12.0
    assert outfit["bundle_price"] < outfit["original_total_price"]
    assert outfit["total_savings"] > 0
    assert len(outfit["one_click_add_payload"]["product_ids"]) == outfit["items_count"]


def test_outfit_generator_laptop_anchor(db_session):
    generator = OutfitBundleGenerator(db_session)
    prod = db_session.query(Product).join(Product.category).filter(Product.category.has(slug="laptops-computing")).first()
    if not prod:
        prod = db_session.query(Product).first()

    outfit = generator.generate_outfit_for_product(product_id=prod.id, bundle_size=3, discount_percentage=15.0)
    assert "error" not in outfit
    assert outfit["bundle_discount_pct"] == 15.0
    assert "Setup" in outfit["theme_title"] or "Ecosystem" in outfit["theme_title"] or "Collection" in outfit["theme_title"]


def test_outfit_generator_not_found(db_session):
    generator = OutfitBundleGenerator(db_session)
    res = generator.generate_outfit_for_product(product_id=999999)
    assert "error" in res


def test_tiered_bundles_generation(db_session):
    recommender = BundleRecommender(db_session)
    prod = db_session.query(Product).first()
    assert prod is not None

    res = recommender.generate_tiered_bundles(product_id=prod.id)
    assert "error" not in res
    assert "tiered_bundles" in res
    assert len(res["tiered_bundles"]) == 3
    tier_names = [b["tier_name"] for b in res["tiered_bundles"]]
    assert "Essential Starter Pair" in tier_names
    assert "Pro Ecosystem Suite" in tier_names
    assert "Ultimate Master Collection" in tier_names


def test_api_outfit_endpoint():
    # Fetch any valid product ID
    prod_res = client.get("/api/v1/products?limit=1")
    assert prod_res.status_code == 200
    res_data = prod_res.json()
    products = res_data if isinstance(res_data, list) else res_data.get("products", [])
    assert len(products) > 0
    prod_id = products[0]["id"]

    res = client.get(f"/api/v1/recommendations-v3/outfit/{prod_id}?bundle_size=3&discount_pct=10.0")
    assert res.status_code == 200
    data = res.json()
    assert data["focal_product_id"] == prod_id
    assert data["bundle_discount_pct"] == 10.0
    assert len(data["items"]) >= 2


def test_api_tiered_bundles_endpoint():
    prod_res = client.get("/api/v1/products?limit=1")
    res_data = prod_res.json()
    products = res_data if isinstance(res_data, list) else res_data.get("products", [])
    prod_id = products[0]["id"]

    res = client.get(f"/api/v1/recommendations-v3/bundles/{prod_id}")
    assert res.status_code == 200
    data = res.json()
    assert "tiered_bundles" in data
    assert len(data["tiered_bundles"]) == 3


def test_api_outfit_not_found():
    res = client.get("/api/v1/recommendations-v3/outfit/999999")
    assert res.status_code == 404
