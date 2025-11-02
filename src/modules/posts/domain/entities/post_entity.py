"""Post Domain Entity."""
from typing import Optional
from src.core.domain.entities import BaseEntity


class PostEntity(BaseEntity):
    """Post domain entity with business logic."""

    def __init__(
        self,
        title: str,
        content: str,
        user_id: int,
        is_published: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.content = content
        self.user_id = user_id
        self.is_published = is_published

    def publish(self) -> None:
        """Business logic: publish post."""
        self.is_published = True

    def unpublish(self) -> None:
        """Business logic: unpublish post."""
        self.is_published = False

    def __repr__(self) -> str:
        return f"PostEntity(id={self.id}, title={self.title})"
