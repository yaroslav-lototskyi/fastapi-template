"""Delete User Use Case."""
from fastapi import HTTPException, status

from src.core.application.use_cases import BaseUseCase
from src.modules.users.domain.repositories import IUserRepository


class DeleteUserUseCase(BaseUseCase[int, bool]):
    """Use case for deleting a user."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> bool:
        """
        Delete user by ID.

        Args:
            user_id: User ID

        Returns:
            True if deleted

        Raises:
            HTTPException: If user not found
        """
        deleted = await self.user_repository.delete(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        return True
