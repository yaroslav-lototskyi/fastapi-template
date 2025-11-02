"""
User Module (Feature Module).

Configures dependency injection for the user feature.
Manages the wiring of repositories, use cases, and controllers.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.modules.users.domain.repositories import IUserRepository
from src.modules.users.infrastructure.persistence import UserRepository
from src.modules.users.application.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    DeleteUserUseCase,
)


class UserModule:
    """
    User feature module.

    Configures dependency injection for:
    - Repositories
    - Use cases
    - Controllers

    This follows Dependency Inversion Principle:
    - Use cases depend on IUserRepository (interface)
    - UserModule provides UserRepository (implementation)
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize module with dependencies.

        In production, you'd use a DI container (like dependency-injector).
        For simplicity, we're doing manual DI here.
        """
        self._db_session = db_session

        # Infrastructure layer
        self._user_repository: IUserRepository = UserRepository(db_session)

    # Factory methods for use cases

    def create_user_use_case(self) -> CreateUserUseCase:
        """Create CreateUserUseCase with injected dependencies."""
        return CreateUserUseCase(self._user_repository)

    def get_user_use_case(self) -> GetUserUseCase:
        """Create GetUserUseCase with injected dependencies."""
        return GetUserUseCase(self._user_repository)

    def list_users_use_case(self) -> ListUsersUseCase:
        """Create ListUsersUseCase with injected dependencies."""
        return ListUsersUseCase(self._user_repository)

    def delete_user_use_case(self) -> DeleteUserUseCase:
        """Create DeleteUserUseCase with injected dependencies."""
        return DeleteUserUseCase(self._user_repository)


# Module instance (singleton pattern)
# In real app, this would be managed by DI container
_user_module_instance = None


async def get_user_module(db: AsyncSession = None) -> UserModule:
    """
    Get UserModule instance.

    This is a simplified DI container.
    In production, use dependency-injector or similar.
    """
    global _user_module_instance

    if db is None:
        # This is called from dependency injection
        from src.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            return UserModule(session)

    return UserModule(db)


# Singleton for easy access (not ideal, but works for demo)
class UserModuleFactory:
    """Factory for creating UserModule with DB session."""

    @staticmethod
    def create_user_use_case():
        """Create use case with DI."""
        from src.core.database import AsyncSessionLocal

        async def _get():
            async with AsyncSessionLocal() as session:
                module = UserModule(session)
                return module.create_user_use_case()

        return _get

    @staticmethod
    def create_get_user_use_case():
        """Create use case with DI."""
        from src.core.database import AsyncSessionLocal

        async def _get():
            async with AsyncSessionLocal() as session:
                module = UserModule(session)
                return module.get_user_use_case()

        return _get


# Simplified access (for controller dependencies)
class user_module:
    """
    Simplified module access.

    Usage in controller:
    use_case = user_module.create_user_use_case()
    """

    @staticmethod
    def create_user_use_case() -> CreateUserUseCase:
        from src.core.database import AsyncSessionLocal

        # Note: This is simplified. In real app, use proper DI container.
        # For now, we'll handle session in the use case execution.

        # We need to create this differently - will fix in controller
        pass

    @staticmethod
    def get_user_use_case() -> GetUserUseCase:
        pass

    @staticmethod
    def list_users_use_case() -> ListUsersUseCase:
        pass

    @staticmethod
    def delete_user_use_case() -> DeleteUserUseCase:
        pass
