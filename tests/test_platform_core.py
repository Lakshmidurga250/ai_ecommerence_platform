"""
Test suite validating platform core, database models, and OpenAPI registry.
"""

import pytest
from app.main import app
from app.core.database import Base

def test_app_initialization():
    """Verify FastAPI application instance initializes with title and version."""
    assert "AI" in app.title
    assert app.version is not None

def test_openapi_schema_generation():
    """Ensure OpenAPI specification generates valid endpoints."""
    schema = app.openapi()
    assert "paths" in schema
    assert len(schema["paths"]) >= 100

def test_database_tables_registered():
    """Verify SQLAlchemy relational models are registered in metadata."""
    import app.models
    assert len(Base.metadata.tables) >= 50
