"""
Domain Exceptions and Centralized Error Handlers.
Prevents leaking internal stack traces while providing consistent JSON error payloads.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger


class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, error_code: str = "BAD_REQUEST", details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details=None):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST, error_code="BAD_REQUEST", details=details)


class AuthenticationException(AppException):
    def __init__(self, message: str = "Invalid credentials or token expired", details=None):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, error_code="AUTHENTICATION_FAILED", details=details)


class AuthorizationException(AppException):
    def __init__(self, message: str = "Insufficient permissions to access this resource", details=None):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN, error_code="FORBIDDEN", details=details)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", identifier: str = "", details=None):
        message = f"{resource} not found" + (f": {identifier}" if identifier else "")
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, error_code="NOT_FOUND", details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict", details=None):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT, error_code="CONFLICT", details=details)


class InsufficientStockException(AppException):
    def __init__(self, product_name: str = "Product", requested: int = 0, available: int = 0):
        message = f"Insufficient stock for '{product_name}'. Requested: {requested}, Available: {available}"
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST, error_code="INSUFFICIENT_STOCK", details={"requested": requested, "available": available})


class PaymentFailedException(AppException):
    def __init__(self, message: str = "Payment simulation failed", transaction_id: str = ""):
        super().__init__(message, status_code=status.HTTP_402_PAYMENT_REQUIRED, error_code="PAYMENT_FAILED", details={"transaction_id": transaction_id})


async def app_exception_handler(request: Request, exc: AppException):
    """Handler for domain exceptions."""
    logger.warning(f"Domain exception: {exc.error_code} - {exc.message} on {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unhandled exceptions (prevents internal stack trace exposure)."""
    logger.exception(f"Unhandled exception on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred. Please try again later.",
                "details": {}
            }
        }
    )

# 401 Unauthorized payload with distinct TOKEN_EXPIRED code
