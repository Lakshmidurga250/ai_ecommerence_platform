"""
Product Catalog & Search Automated Test Suite.
"""

def test_list_products(client):
    res = client.get("/api/v1/products/")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5
    first = data[0]
    assert "name" in first
    assert "price" in first
    assert "stock" in first


def test_product_price_filtering(client):
    res = client.get("/api/v1/products/?min_price=100000&max_price=250000")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    for p in data:
        assert 100000 <= p["price"] <= 250000


def test_search_products(client):
    res = client.get("/api/v1/search/?q=macbook")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert "macbook" in data[0]["name"].lower()


def test_search_suggestions(client):
    res = client.get("/api/v1/search/suggestions?prefix=app")
    assert res.status_code == 200
    suggestions = res.json()
    assert isinstance(suggestions, list)
    assert any("apple" in s.lower() for s in suggestions)


def test_categories_and_brands(client):
    cat_res = client.get("/api/v1/categories/")
    assert cat_res.status_code == 200
    assert len(cat_res.json()) >= 4

    brand_res = client.get("/api/v1/categories/brands")
    assert brand_res.status_code == 200
    assert len(brand_res.json()) >= 4
