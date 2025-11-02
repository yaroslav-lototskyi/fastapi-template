"""
User module dependencies for FastAPI.
Separates DI concerns from presentation layer.
"""
from src.core.infrastructure.container import (
    get_logger as _get_logger,
    get_notification_service as _get_notification_service,
)


async def get_logger():
    """Get logger for user endpoints."""
    return await _get_logger()


async def get_notification():
    """Get notification service for user endpoints."""
    return await _get_notification_service()
