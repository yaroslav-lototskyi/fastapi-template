"""
Create User Use Case.

Use Case = application-specific business rule.
Each use case does ONE thing (Single Responsibility Principle).

Steps:
1. Check if user exists
2. Create user entity
3. Save user via repository
4. Return response DTO
"""
from fastapi import HTTPException, status

from src.core.application.use_cases import BaseUseCase
from src.modules.users.application.dto import CreateUserDto, UserResponseDto
from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import IUserRepository


class CreateUserUseCase(BaseUseCase[CreateUserDto, UserResponseDto]):
    """
    Use case for creating a user.

    Dependencies:
    - IUserRepository (injected via DI)

    Steps:
    1. Validate business rules
    2. Create domain entity
    3. Save via repository
    4. Return DTO
    """

    def __init__(self, user_repository: IUserRepository):
        """
        Constructor with dependency injection.

        Args:
            user_repository: Repository for user data access operations
        """
        self.user_repository = user_repository

    async def execute(self, input_dto: CreateUserDto) -> UserResponseDto:
        """
        Execute the use case.

        Args:
            input_dto: Create user data

        Returns:
            Created user

        Raises:
            HTTPException: If email or username already exists
        """
        # 1. Business rule: email must be unique
        if await self.user_repository.email_exists(input_dto.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # 2. Business rule: username must be unique
        if await self.user_repository.username_exists(input_dto.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # 3. Create domain entity
        user_entity = UserEntity(
            email=input_dto.email,
            username=input_dto.username,
            full_name=input_dto.full_name,
        )

        # 4. Save via repository
        created_user = await self.user_repository.create(user_entity)

        # 5. Convert entity to DTO
        return self._entity_to_dto(created_user)

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
