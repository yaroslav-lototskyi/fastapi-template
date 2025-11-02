"""
Base Repository Interface (Clean Architecture).

Repository pattern: interface between domain layer and data access layer.
Defines standard CRUD operations for all repositories.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

from src.core.domain.entities import BaseEntity

# Generic type for Entity
EntityType = TypeVar("EntityType", bound=BaseEntity)


class BaseRepository(ABC, Generic[EntityType]):
    """
    Base repository interface.

    In Clean Architecture:
    - Repository is an interface (abstract class)
    - Domain layer defines the interface
    - Infrastructure layer provides the implementation
    - Follows Dependency Inversion Principle (SOLID)
    """

    @abstractmethod
    async def create(self, entity: EntityType) -> EntityType:
        """Create a new entity."""
        pass

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[EntityType]:
        """Find entity by ID."""
        pass

    @abstractmethod
    async def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[EntityType], int]:
        """Find all entities with pagination."""
        pass

    @abstractmethod
    async def update(self, id: int, entity: EntityType) -> Optional[EntityType]:
        """Update entity."""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete entity."""
        pass
