"""
Structured Logger Service (Singleton).

Production-ready logging with structlog.
Provides structured JSON logging for production and human-readable logs for development.
"""
import sys
import structlog
from typing import Any
from structlog.types import FilteringBoundLogger


class LoggerService:
    """
    Structured logger service.

    Features:
    - Structured JSON logging for production
    - Human-readable console output for development
    - Context propagation and binding
    - Async-friendly
    - Request ID tracking
    """

    def __init__(self, env: str = "development"):
        """
        Initialize logger.

        Args:
            env: Environment (development/production)
        """
        self.env = env
        self._configure_structlog()
        self.logger: FilteringBoundLogger = structlog.get_logger()

    def _configure_structlog(self) -> None:
        """Configure structlog processors and renderers."""
        # Development: human-readable console output
        # Production: JSON for log aggregation (ELK, DataDog, etc.)

        shared_processors = [
            # Add log level
            structlog.stdlib.add_log_level,
            # Add timestamp
            structlog.processors.TimeStamper(fmt="iso"),
            # Add caller info (file, line, function)
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
        ]

        if self.env == "production":
            # JSON output for production
            processors = shared_processors + [
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(),
            ]
        else:
            # Colored console output for development
            processors = shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True),
            ]

        structlog.configure(
            processors=processors,
            wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
            cache_logger_on_first_use=True,
        )

    def bind(self, **kwargs: Any) -> FilteringBoundLogger:
        """
        Bind context to logger.

        Usage:
            logger = logger_service.bind(request_id="123", user_id=456)
            logger.info("User action", action="login")
            # Output: {..., "request_id": "123", "user_id": 456, "action": "login"}
        """
        return self.logger.bind(**kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        """
        Log info message.

        Args:
            event: Log message
            **kwargs: Additional context
        """
        self.logger.info(event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        """
        Log error message.

        Args:
            event: Error message
            **kwargs: Additional context (exc_info for stack trace)
        """
        self.logger.error(event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(event, **kwargs)

    def debug(self, event: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(event, **kwargs)

    def exception(self, event: str, exc_info: Exception, **kwargs: Any) -> None:
        """
        Log exception with stack trace.

        Args:
            event: Error message
            exc_info: Exception instance
            **kwargs: Additional context
        """
        self.logger.error(event, exc_info=exc_info, **kwargs)


# Example usage:
#
# logger = LoggerService(env="development")
#
# # Simple log
# logger.info("Application started", version="1.0.0")
#
# # With context binding
# request_logger = logger.bind(request_id="abc-123", user_id=42)
# request_logger.info("User login", email="test@example.com")
# request_logger.info("User fetched profile")
#
# # Error with exception
# try:
#     1 / 0
# except Exception as e:
#     logger.exception("Division error", exc_info=e, operation="divide")
