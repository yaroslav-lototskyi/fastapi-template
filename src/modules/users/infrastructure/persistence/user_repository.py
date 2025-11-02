"""
User Repository Implementation (Infrastructure Layer).

Implements IUserRepository interface from domain layer.
Uses SQLAlchemy for database operations.

This follows Dependency Inversion Principle:
- Domain defines interface (IUserRepository)
- Infrastructure implements interface (UserRepository)
- Use cases depend on interface, not implementation
"""
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import IUserRepository
from .user_model import UserModel


class UserRepository(IUserRepository):
    """
    SQLAlchemy implementation of IUserRepository.

    Provides concrete implementation of the user repository interface
    using SQLAlchemy for database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Constructor with database session injection.

        Args:
            session: SQLAlchemy async session for database operations
        """
        self.session = session

    async def create(self, entity: UserEntity) -> UserEntity:
        """Create a new user."""
        # Convert domain entity to database model
        model = self._entity_to_model(entity)

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        # Convert database model back to domain entity
        return self._model_to_entity(model)

    async def find_by_id(self, id: int) -> Optional[UserEntity]:
        """Find user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[UserEntity], int]:
        """Find all users with pagination."""
        # Get total count
        count_result = await self.session.execute(select(func.count(UserModel.id)))
        total = count_result.scalar_one()

        # Get paginated users
        result = await self.session.execute(
            select(UserModel).order_by(UserModel.created_at.desc()).offset(skip).limit(limit)
        )
        models = list(result.scalars().all())

        entities = [self._model_to_entity(model) for model in models]
        return entities, total

    async def update(self, id: int, entity: UserEntity) -> Optional[UserEntity]:
        """Update user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        # Update model from entity
        model.email = entity.email
        model.username = entity.username
        model.full_name = entity.full_name
        model.is_active = entity.is_active

        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, id: int) -> bool:
        """Delete user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return False

        await self.session.delete(model)
        await self.session.flush()
        return True

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        """Find user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def find_by_username(self, username: str) -> Optional[UserEntity]:
        """Find user by username."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def email_exists(self, email: str) -> bool:
        """Check if email exists."""
        result = await self.session.execute(
            select(func.count(UserModel.id)).where(UserModel.email == email)
        )
        count = result.scalar_one()
        return count > 0

    async def username_exists(self, username: str) -> bool:
        """Check if username exists."""
        result = await self.session.execute(
            select(func.count(UserModel.id)).where(UserModel.username == username)
        )
        count = result.scalar_one()
        return count > 0

    # Mappers

    def _entity_to_model(self, entity: UserEntity) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def _model_to_entity(self, model: UserModel) -> UserEntity:
        """Convert database model to domain entity."""
        return UserEntity(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
