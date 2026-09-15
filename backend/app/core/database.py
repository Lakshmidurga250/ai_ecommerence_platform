"""
Database Connection & Session Management Module.
Supports PostgreSQL in production / Docker with seamless SQLite fallback for standalone development.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine configuration
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DB_ECHO,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=settings.DB_ECHO,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency for yielding database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Check if the database is accessible."""
    try:
        with engine.connect() as conn:
            conn.execute(Base.metadata.tables.get("users", None) or "SELECT 1")
        return True
    except Exception:
        # Fallback check
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

# PRAGMA journal_mode=WAL and synchronous=NORMAL optimization
