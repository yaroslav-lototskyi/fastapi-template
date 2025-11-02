"""List Users Use Case."""
from src.core.application.use_cases import BaseUseCase
from src.modules.users.application.dto import UserListResponseDto, UserResponseDto
from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import IUserRepository


class ListUsersInput:
    """Input for list users use case."""

    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size


class ListUsersUseCase(BaseUseCase[ListUsersInput, UserListResponseDto]):
    """Use case for listing users with pagination."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, input_dto: ListUsersInput) -> UserListResponseDto:
        """
        List users with pagination.

        Args:
            input_dto: Pagination parameters

        Returns:
            Paginated list of users
        """
        skip = (input_dto.page - 1) * input_dto.page_size
        limit = input_dto.page_size

        users, total = await self.user_repository.find_all(skip=skip, limit=limit)

        return UserListResponseDto(
            items=[self._entity_to_dto(user) for user in users],
            total=total,
            page=input_dto.page,
            page_size=input_dto.page_size,
        )

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
