"""Email service for sending emails."""


class EmailService:
    """Email service (stateless, Singleton)."""

    def __init__(self, smtp_host: str = "localhost", smtp_port: int = 587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    async def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send email (mock for now)."""
        # TODO: Implement real email sending (SMTP, SendGrid, etc.)
        return {"status": "sent", "to": to}
