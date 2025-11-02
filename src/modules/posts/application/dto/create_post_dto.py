"""Create Post DTO."""
from pydantic import BaseModel, Field


class CreatePostDto(BaseModel):
    """DTO for creating a post."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    user_id: int = Field(..., gt=0)
    is_published: bool = False
