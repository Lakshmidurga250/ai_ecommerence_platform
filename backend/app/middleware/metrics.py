"""
Prometheus Metrics Instrumentation Middleware.
Tracks HTTP requests, duration, status codes, and ML inference metrics.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Metrics definitions
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests processed",
    ["method", "endpoint", "status_code"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_CONNECTIONS = Gauge(
    "http_active_connections",
    "Number of active HTTP connections currently being processed"
)

ML_INFERENCE_COUNT = Counter(
    "ml_inference_total",
    "Total machine learning inferences executed",
    ["model_name", "status"]
)

ML_INFERENCE_LATENCY = Histogram(
    "ml_inference_duration_seconds",
    "Latency of ML model inferences",
    ["model_name"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in ("/metrics", "/health"):
            return await call_next(request)

        ACTIVE_CONNECTIONS.inc()
        start_time = time.time()
        method = request.method
        endpoint = request.url.path

        try:
            response = await call_next(request)
            duration = time.time() - start_time
            HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status_code=response.status_code).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status_code=500).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(duration)
            raise e
        finally:
            ACTIVE_CONNECTIONS.dec()


def metrics_endpoint_handler():
    """Handler returning formatted Prometheus metrics text."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
