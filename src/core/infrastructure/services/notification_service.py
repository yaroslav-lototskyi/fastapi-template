"""Notification service for sending notifications via multiple channels."""

from src.core.infrastructure.services.email_service import EmailService
from src.core.infrastructure.services.logger_service import LoggerService
from src.core.infrastructure.services.sms_service import SMSService


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
