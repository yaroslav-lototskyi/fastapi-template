"""Post Response DTO."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostResponseDto(BaseModel):
    """DTO for post responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    user_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class PostListResponseDto(BaseModel):
    """DTO for paginated post list."""

    items: list[PostResponseDto]
    total: int
    page: int
    page_size: int
