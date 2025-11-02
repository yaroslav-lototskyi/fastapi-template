"""Post Repository Interface."""
from abc import abstractmethod
from typing import Optional, List

from src.core.domain.repositories import BaseRepository
from src.modules.posts.domain.entities import PostEntity


class IPostRepository(BaseRepository[PostEntity]):
    """Post repository interface."""

    @abstractmethod
    async def find_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[List[PostEntity], int]:
        """Find posts by user ID."""
        pass

    @abstractmethod
    async def find_published(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[PostEntity], int]:
        """Find only published posts."""
        pass
