"""
Authentication & RBAC Automated Test Suite.
"""

import uuid
import pytest


def test_user_registration(client):
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    unique_user = f"user_{uuid.uuid4().hex[:6]}"
    res = client.post("/api/v1/auth/register", json={
        "email": unique_email,
        "username": unique_user,
        "password": "SecurePassword@123",
        "role": "CUSTOMER",
        "first_name": "Test",
        "last_name": "Shopper"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == unique_email
    assert data["username"] == unique_user
    assert "CUSTOMER" in data["roles"]


def test_login_success(client):
    res = client.post("/api/v1/auth/login", json={
        "email_or_username": "john.doe@example.com",
        "password": "Customer@123456"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    res = client.post("/api/v1/auth/login", json={
        "email_or_username": "john.doe@example.com",
        "password": "WrongPassword999"
    })
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "AUTHENTICATION_FAILED"


def test_refresh_token(client):
    login_res = client.post("/api/v1/auth/login", json={
        "email_or_username": "john.doe@example.com",
        "password": "Customer@123456"
    })
    refresh_token = login_res.json()["refresh_token"]

    res = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_rbac_admin_route_forbidden_for_customer(client, customer_token):
    res = client.get("/api/v1/admin/audit-logs", headers={"Authorization": f"Bearer {customer_token}"})
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"


def test_rbac_admin_route_allowed_for_admin(client, admin_token):
    res = client.get("/api/v1/admin/audit-logs", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)
