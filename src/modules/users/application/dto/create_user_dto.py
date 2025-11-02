"""
Create User DTO (Data Transfer Object).

DTO = object that carries data between processes.
Uses Pydantic for validation and type safety.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserDto(BaseModel):
    """
    DTO for creating a user.

    Includes validation rules:
    - email: Must be a valid email address
    - username: 3-50 characters
    - full_name: Optional, max 255 characters
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
            }
        }
    )

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
