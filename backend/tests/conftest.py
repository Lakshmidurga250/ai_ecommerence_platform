"""
Pytest Fixtures and Test Environment Setup.
"""

import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.main import app
from app.core.database import SessionLocal, Base, engine
from database.seeds.seed_data import seed_database


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure database schema and seed data are loaded for tests."""
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def customer_token(client):
    """Authenticate standard customer."""
    res = client.post("/api/v1/auth/login", json={
        "email_or_username": "john.doe@example.com",
        "password": "Customer@123456"
    })
    return res.json()["access_token"]


@pytest.fixture
def seller_token(client):
    """Authenticate marketplace seller."""
    res = client.post("/api/v1/auth/login", json={
        "email_or_username": "seller1@techvault.com",
        "password": "Seller@123456"
    })
    return res.json()["access_token"]


@pytest.fixture
def admin_token(client):
    """Authenticate platform admin."""
    res = client.post("/api/v1/auth/login", json={
        "email_or_username": "admin@platform.com",
        "password": "Admin@123456"
    })
    return res.json()["access_token"]


@pytest.fixture
def db_session():
    """Direct database session fixture for services testing."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

