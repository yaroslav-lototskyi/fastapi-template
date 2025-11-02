"""
User Module Providers (Dependency Injection).

This file contains provider functions for FastAPI Depends().
Provides dependency injection for repositories and use cases.
"""
from fastapi import Depends
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


# Repository providers


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> IUserRepository:
    """
    Provide IUserRepository implementation.

    Returns UserRepository with database session.
    """
    return UserRepository(db)


# Use case providers


def get_create_user_use_case(
    user_repository: IUserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    """
    Provide CreateUserUseCase with injected dependencies.

    Dependency chain:
    CreateUserUseCase -> IUserRepository -> AsyncSession
    """
    return CreateUserUseCase(user_repository)


def get_get_user_use_case(
    user_repository: IUserRepository = Depends(get_user_repository),
) -> GetUserUseCase:
    """Provide GetUserUseCase with injected dependencies."""
    return GetUserUseCase(user_repository)


def get_list_users_use_case(
    user_repository: IUserRepository = Depends(get_user_repository),
) -> ListUsersUseCase:
    """Provide ListUsersUseCase with injected dependencies."""
    return ListUsersUseCase(user_repository)


def get_delete_user_use_case(
    user_repository: IUserRepository = Depends(get_user_repository),
) -> DeleteUserUseCase:
    """Provide DeleteUserUseCase with injected dependencies."""
    return DeleteUserUseCase(user_repository)
