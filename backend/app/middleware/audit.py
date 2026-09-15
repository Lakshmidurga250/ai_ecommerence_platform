"""
Audit Logging Middleware.
Captures mutating API operations and records them to the audit trail.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.database import SessionLocal
from app.core.security import decode_token
from app.models.audit import AuditLog
from app.core.logging import logger


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Only audit mutating methods (POST, PUT, PATCH, DELETE)
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            path = request.url.path
            # Avoid auditing metrics and health
            if not path.startswith(("/metrics", "/health", "/docs", "/openapi.json")):
                user_id = None
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    payload = decode_token(token)
                    if payload:
                        user_id = payload.get("sub") or payload.get("user_id")
                        try:
                            user_id = int(user_id) if user_id else None
                        except (ValueError, TypeError):
                            user_id = None

                client_ip = request.client.host if request.client else None
                user_agent = request.headers.get("User-Agent")
                status = "SUCCESS" if response.status_code < 400 else ("FORBIDDEN" if response.status_code == 403 else "FAILURE")

                # Asynchronously record or commit to audit log
                try:
                    db = SessionLocal()
                    try:
                        audit_entry = AuditLog(
                            user_id=user_id,
                            action=f"{request.method} {path}",
                            resource_type=path.split("/")[3] if len(path.split("/")) > 3 else "system",
                            ip_address=client_ip,
                            user_agent=user_agent[:250] if user_agent else None,
                            status=status,
                            details={"status_code": response.status_code}
                        )
                        db.add(audit_entry)
                        db.commit()
                    finally:
                        db.close()
                except Exception as ex:
                    logger.debug(f"Audit log recording error: {ex}")

        return response

# Audit log structured json formatting with user context
