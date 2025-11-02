"""
Application DI Container - Hybrid Approach.

Combines dependency-injector for stateless Singleton services
with FastAPI Depends for stateful per-request services.
"""
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from src.core.infrastructure.logger import LoggerService


# ==========================================
# Stateless Services (Singleton)
# ==========================================

class EmailService:
    """Email service (stateless, Singleton)."""

    def __init__(self, smtp_host: str = "localhost", smtp_port: int = 587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    async def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send email (mock for now)."""
        # TODO: Implement real email sending (SMTP, SendGrid, etc.)
        return {"status": "sent", "to": to}


class SMSService:
    """SMS service (stateless, Singleton)."""

    def __init__(self, api_key: str = "default_key"):
        self.api_key = api_key

    async def send_sms(self, to: str, message: str) -> dict:
        """Send SMS (mock for now)."""
        # TODO: Implement real SMS (Twilio, etc.)
        return {"status": "sent", "to": to}


class NotificationService:
    """Notification service with dependencies."""

    def __init__(
        self,
        logger: LoggerService,
        email_service: EmailService,
        sms_service: SMSService,
    ):
        self.logger = logger
        self.email_service = email_service
        self.sms_service = sms_service

    async def notify(self, user_id: int, message: str) -> None:
        """
        Send notification via email and SMS.

        Args:
            user_id: User ID
            message: Notification message
        """
        self.logger.info(
            "Sending notification",
            user_id=user_id,
            message=message,
            service="notification",
        )

        # Send email
        await self.email_service.send_email(
            to=f"user{user_id}@example.com",
            subject="Notification",
            body=message,
        )

        # Send SMS
        await self.sms_service.send_sms(to=f"+123456789", message=message)

        self.logger.info("Notification sent", user_id=user_id)


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
