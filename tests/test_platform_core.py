"""
Test suite validating platform core, database models, and OpenAPI registry.
"""

import sys
from pathlib import Path

# Ensure workspace root and backend directory are in sys.path
_ROOT = Path(__file__).resolve().parent.parent
for _p in (str(_ROOT), str(_ROOT / "backend")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pytest

try:
    from app.main import app as fastapi_app
    from app.core.database import Base
    import app.models as _models
except ImportError:
    from backend.app.main import app as fastapi_app
    from backend.app.core.database import Base
    import backend.app.models as _models


def test_app_initialization():
    """Verify FastAPI application instance initializes with title and version."""
    assert "AI" in fastapi_app.title
    assert fastapi_app.version is not None


def test_openapi_schema_generation():
    """Ensure OpenAPI specification generates valid endpoints."""
    schema = fastapi_app.openapi()
    assert "paths" in schema
    assert len(schema["paths"]) >= 100


def test_database_tables_registered():
    """Verify SQLAlchemy relational models are registered in metadata."""
    assert len(Base.metadata.tables) >= 50


if __name__ == "__main__":
    test_app_initialization()
    test_openapi_schema_generation()
    test_database_tables_registered()
    print("All platform core tests passed successfully.")


