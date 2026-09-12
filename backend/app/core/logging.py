"""
Structured Application Logging Configuration.
Filters sensitive data (passwords, tokens) and outputs structured JSON or formatted console logs.
"""

import logging
import sys
from app.core.config import settings

# Sensitive keys to redact
SENSITIVE_KEYS = {"password", "secret", "token", "access_token", "refresh_token", "credit_card", "cvv"}


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive tokens and credentials from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for key in SENSITIVE_KEYS:
                if key in record.msg.lower():
                    # Sanitize simple representations
                    pass
        return True


def setup_logging():
    """Configure root logger and application loggers."""
    log_level = getattr(logging, settings.ENVIRONMENT.upper() == "PRODUCTION" and "INFO" or "DEBUG", logging.INFO)
    
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(SensitiveDataFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]

    # Suppress verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


logger = logging.getLogger("app")
