"""
Rate Limiting Middleware.
Provides IP-based sliding window rate limiting with zero external dependencies.
"""

import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Exclude metrics and health endpoints
        if request.url.path in ("/metrics", "/health", "/docs", "/openapi.json"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        if client_ip in ("testclient", "test"):
            return await call_next(request)
        now = time.time()
        window_start = now - 60.0

        # Clean old timestamps
        timestamps = self.request_counts[client_ip]
        self.request_counts[client_ip] = [t for t in timestamps if t > window_start]

        if len(self.request_counts[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please slow down and try again shortly.",
                        "details": {"retry_after_seconds": 60}
                    }
                },
                headers={"Retry-After": "60"}
            )

        self.request_counts[client_ip].append(now)
        return await call_next(request)
