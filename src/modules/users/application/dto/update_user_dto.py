"""Update User DTO."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UpdateUserDto(BaseModel):
    """
    DTO for updating a user.

    All fields are optional to support partial updates.
    Only provided fields will be updated.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Updated",
                "is_active": False,
            }
        }
    )

    email: Optional[EmailStr] = Field(None, description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = Field(None, description="Active status")
