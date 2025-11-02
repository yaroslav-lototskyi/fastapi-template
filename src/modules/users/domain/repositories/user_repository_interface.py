"""
User Repository Interface (Domain Layer).

Interface = contract that infrastructure must implement.
This follows Dependency Inversion Principle (SOLID).

The domain layer defines the contract (interface),
while the infrastructure layer provides the concrete implementation.
"""
from abc import abstractmethod
from typing import Optional

from src.core.domain.repositories import BaseRepository
from src.modules.users.domain.entities import UserEntity


class IUserRepository(BaseRepository[UserEntity]):
    """
    User repository interface.

    Domain layer defines WHAT operations are needed.
    Infrastructure layer defines HOW to implement them.

    This is Dependency Inversion Principle:
    - High-level modules (use cases) depend on abstractions (interfaces)
    - Low-level modules (repositories) implement abstractions
    """

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        """Find user by email."""
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[UserEntity]:
        """Find user by username."""
        pass

    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        pass

    @abstractmethod
    async def username_exists(self, username: str) -> bool:
        """Check if username already exists."""
        pass
