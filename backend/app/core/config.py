"""
Application Configuration Module.
Supports environment variables and .env file loading with safe defaults.
"""

import os
from pathlib import Path
from typing import List

import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
ENV_FILE = BASE_DIR / ".env"

# Load .env file manually if exists
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key not in os.environ:
                    os.environ[key] = val


class Settings:
    # Application Info
    APP_NAME: str = os.getenv("APP_NAME", "AI E-Commerce & Recommendation Platform")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")

    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'ecommerce.db').as_posix()}")
    DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() in ("true", "1", "yes")

    # Redis / Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False").lower() in ("true", "1", "yes")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    # Search & Elasticsearch
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_ENABLED: bool = os.getenv("ELASTICSEARCH_ENABLED", "False").lower() in ("true", "1", "yes")
    ELASTICSEARCH_INDEX_PREFIX: str = os.getenv("ELASTICSEARCH_INDEX_PREFIX", "ecommerce_")

    # Storage
    LOCAL_STORAGE_DIR: str = os.getenv("LOCAL_STORAGE_DIR", str(BASE_DIR / "storage"))
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "ecommerce-assets")

    # AI & ML
    MODEL_REGISTRY_DIR: str = os.getenv("MODEL_REGISTRY_DIR", str(BASE_DIR / "ai" / "model_registry" / "artifacts"))
    DEFAULT_RECOMMENDATION_COUNT: int = int(os.getenv("DEFAULT_RECOMMENDATION_COUNT", "10"))
    ANOMALY_DETECTION_THRESHOLD: float = float(os.getenv("ANOMALY_DETECTION_THRESHOLD", "0.65"))
    CHURN_THRESHOLD_DAYS: int = int(os.getenv("CHURN_THRESHOLD_DAYS", "60"))

    # CORS & Middleware
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))
    PROMETHEUS_METRICS_ENABLED: bool = os.getenv("PROMETHEUS_METRICS_ENABLED", "True").lower() in ("true", "1", "yes")


settings = Settings()
