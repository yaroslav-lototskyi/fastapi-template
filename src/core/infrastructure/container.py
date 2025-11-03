"""
Application DI Container - Hybrid Approach.

Combines dependency-injector for stateless Singleton services
with FastAPI Depends for stateful per-request services.
"""
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from src.core.infrastructure.services import (
    EmailService,
    LoggerService,
    NotificationService,
    SMSService,
)


# ==========================================
# Application DI Container
# ==========================================


class ApplicationContainer(containers.DeclarativeContainer):
    """
    Application-wide DI Container.

    Manages Singleton stateless services.
    Stateful services (DB, repositories, use cases) use FastAPI Depends().
    """

    # Configuration
    config = providers.Configuration()

    # ==========================================
    # Core Services (Singleton)
    # ==========================================

    # Logger (Singleton) - available everywhere
    logger = providers.Singleton(
        LoggerService,
        env=config.app_env,
    )

    # Email Service (Singleton)
    email_service = providers.Singleton(
        EmailService,
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
    )

    # SMS Service (Singleton)
    sms_service = providers.Singleton(
        SMSService,
        api_key=config.sms_api_key,
    )

    # Notification Service (Singleton) - depends on logger, email, sms
    notification_service = providers.Singleton(
        NotificationService,
        logger=logger,
        email_service=email_service,
        sms_service=sms_service,
    )


# ==========================================
# FastAPI Integration Helpers
# ==========================================


@inject
async def get_logger(
    logger: LoggerService = Provide[ApplicationContainer.logger],
):
    """
    Get logger service for FastAPI Depends.

    Usage in controller:
        async def endpoint(logger: LoggerService = Depends(get_logger)):
            logger.info("Request received")
    """
    return logger


@inject
async def get_notification_service(
    service: NotificationService = Provide[ApplicationContainer.notification_service],
):
    """
    Get notification service for FastAPI Depends.

    Usage in controller:
        async def endpoint(
            notifier: NotificationService = Depends(get_notification_service)
        ):
            await notifier.notify(user_id, "Hello")
    """
    return service


# Export only what's needed for FastAPI
__all__ = [
    "ApplicationContainer",
    "get_logger",
    "get_notification_service",
]
