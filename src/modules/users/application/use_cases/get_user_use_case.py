"""Get User Use Case."""
from typing import Optional
from fastapi import HTTPException, status

from src.core.application.use_cases import BaseUseCase
from src.modules.users.application.dto import UserResponseDto
from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import IUserRepository


class GetUserUseCase(BaseUseCase[int, UserResponseDto]):
    """Use case for getting a user by ID."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> UserResponseDto:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User data

        Raises:
            HTTPException: If user not found
        """
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        return self._entity_to_dto(user)

    def _entity_to_dto(self, entity: UserEntity) -> UserResponseDto:
        """Convert domain entity to response DTO."""
        return UserResponseDto(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
