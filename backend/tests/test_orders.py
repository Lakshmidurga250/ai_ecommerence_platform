"""
Cart, Coupon, and Checkout Automated Test Suite.
"""

def test_cart_lifecycle(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    
    # 1. Clear cart
    client.delete("/api/v1/cart/", headers=headers)

    # 2. Get first product
    prods = client.get("/api/v1/products/").json()
    prod_id = prods[0]["id"]

    # 3. Add to cart
    add_res = client.post("/api/v1/cart/items", json={"product_id": prod_id, "quantity": 2}, headers=headers)
    assert add_res.status_code == 201
    cart = add_res.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["quantity"] == 2
    assert cart["subtotal"] > 0
    assert cart["total_amount"] > 0

    # 4. Update quantity
    item_id = cart["items"][0]["id"]
    upd_res = client.put(f"/api/v1/cart/items/{item_id}", json={"quantity": 3}, headers=headers)
    assert upd_res.status_code == 200
    assert upd_res.json()["items"][0]["quantity"] == 3

    # 5. Remove item
    del_res = client.delete(f"/api/v1/cart/items/{item_id}", headers=headers)
    assert del_res.status_code == 200
    assert len(del_res.json()["items"]) == 0


def test_coupon_validation(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    res = client.post("/api/v1/coupons/validate", json={"code": "FESTIVE20", "cart_total": 4000.0}, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["code"] == "FESTIVE20"
    assert data["discount_value"] == 20.0


def test_checkout_and_order_placement(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    
    # Add item
    prods = client.get("/api/v1/products/").json()
    prod_id = prods[0]["id"]
    client.post("/api/v1/cart/items", json={"product_id": prod_id, "quantity": 1}, headers=headers)

    # Get address
    addrs = client.get("/api/v1/users/addresses", headers=headers).json()
    assert len(addrs) > 0
    addr_id = addrs[0]["id"]

    # Checkout
    order_res = client.post("/api/v1/orders/checkout", json={
        "shipping_address_id": addr_id,
        "payment_method": "CARD",
        "coupon_code": "WELCOME10"
    }, headers=headers)

    assert order_res.status_code == 201
    order = order_res.json()
    assert "order_number" in order
    assert order["status"] == "CONFIRMED"
    assert order["total_amount"] > 0
    assert len(order["payments"]) == 1
    assert order["payments"][0]["status"] == "SUCCESS"
    assert order["shipment"] is not None
    assert order["shipment"]["tracking_number"] is not None
