"""SMS service for sending SMS messages."""


class SMSService:
    """SMS service (stateless, Singleton)."""

    def __init__(self, api_key: str = "default_key"):
        self.api_key = api_key

    async def send_sms(self, to: str, message: str) -> dict:
        """Send SMS (mock for now)."""
        # TODO: Implement real SMS (Twilio, etc.)
        return {"status": "sent", "to": to}
