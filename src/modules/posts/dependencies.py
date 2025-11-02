"""
Post module dependencies for FastAPI.
"""
from src.core.infrastructure.container import get_logger as _get_logger


async def get_logger():
    """Get logger for post endpoints."""
    return await _get_logger()
