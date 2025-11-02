"""User Response DTO."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponseDto(BaseModel):
    """
    DTO for user responses.

    Used when returning user data from API endpoints.
    Contains all user fields safe for public exposure.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
            }
        }
    )

    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserListResponseDto(BaseModel):
    """DTO for paginated user list."""

    items: list[UserResponseDto]
    total: int
    page: int
    page_size: int
