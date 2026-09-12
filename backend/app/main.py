"""
FastAPI Application Entrypoint.
Initializes middleware, routers, exception handlers, WebSockets, and health checks.
"""

from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.core.database import Base, engine, check_db_connection
from app.middleware import PrometheusMetricsMiddleware, metrics_endpoint_handler, RateLimitMiddleware, AuditLoggingMiddleware
from app.api.v1 import api_v1_router
from app.websocket.manager import ws_manager
from app.services.search_service import SearchService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup structured logging
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} in {settings.ENVIRONMENT} mode")
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Initialize in-memory search index
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        SearchService.sync_index(db)
        db.close()
    except Exception as e:
        logger.warning(f"Initial search index synchronization deferred: {e}")
        
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Multi-Vendor E-Commerce & Recommendation Platform API",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.PROMETHEUS_METRICS_ENABLED:
    app.add_middleware(PrometheusMetricsMiddleware)
    app.add_api_route("/metrics", metrics_endpoint_handler, methods=["GET"], include_in_schema=False)

app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)
app.add_middleware(AuditLoggingMiddleware)

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Include API v1 Router
app.include_router(api_v1_router)


# Health check endpoint
@app.get("/health", tags=["System Health"])
def health_check():
    """System health check endpoint verifying database connectivity."""
    db_ok = check_db_connection()
    return {
        "status": "HEALTHY" if db_ok else "DEGRADED",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database_connected": db_ok,
        "environment": settings.ENVIRONMENT
    }


# Real-time WebSocket Endpoint
@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    """
    WebSocket connection endpoint for real-time order tracking and alerts.
    Subscribes client to specified topic (e.g., 'order_12', 'admin_channel', 'user_5').
    """
    await ws_manager.connect(websocket, topic)
    try:
        while True:
            # Keep-alive heartbeat listener
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, topic)
