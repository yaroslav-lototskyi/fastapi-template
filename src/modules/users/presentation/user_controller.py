"""
User Controller - Hybrid DI Approach.

Stateless services (logger, notification) → Singleton via container
Stateful services (DB, repository, use cases) → Per-request via Depends
"""
from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from src.modules.users.dependencies import get_logger, get_notification
from src.modules.users.application.dto import (
    CreateUserDto,
    UserResponseDto,
    UserListResponseDto,
)
from src.modules.users.application.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    ListUsersInput,
    DeleteUserUseCase,
)
from src.modules.users.user_providers import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_list_users_use_case,
    get_delete_user_use_case,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# ==========================================
# Create User
# ==========================================


@router.post(
    "",
    response_model=UserResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    dto: CreateUserDto,
    # Stateful (per-request) - dependency chain via Depends
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    # Stateless (singleton) - via container
    logger=Depends(get_logger),
    notification=Depends(get_notification),
):
    """
    Create new user - Hybrid DI approach.

    Stateful chain: DB → Repository → UseCase (per-request)
    Stateless: Logger, Notification (singleton)
    """
    logger.info("Creating user", email=dto.email, username=dto.username)

    # Execute use case - NO manual instantiation!
    user = await use_case.execute(dto)

    logger.info("User created", user_id=user.id, email=user.email)

    # Send notification (async)
    await notification.notify(user.id, f"Welcome {user.username}!")

    return user


# ==========================================
# List Users
# ==========================================


@router.get(
    "",
    response_model=UserListResponseDto,
    summary="Get all users",
)
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
    logger=Depends(get_logger),
):
    """
    Get paginated list of users with pagination support.
    """
    logger.info("Listing users", page=page, page_size=page_size)

    input_dto = ListUsersInput(page=page, page_size=page_size)
    result = await use_case.execute(input_dto)

    logger.info("Users listed", count=len(result.items), total=result.total)
    return result


# ==========================================
# Get User by ID
# ==========================================


@router.get(
    "/{user_id}",
    response_model=UserResponseDto,
    summary="Get user by ID",
)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
    logger=Depends(get_logger),
):
    """
    Get a specific user by ID.
    """
    logger.info("Fetching user", user_id=user_id)

    user = await use_case.execute(user_id)

    logger.info("User fetched", user_id=user.id, email=user.email)
    return user


# ==========================================
# Delete User
# ==========================================


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete user",
)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
    logger=Depends(get_logger),
):
    """
    Delete user by ID.
    """
    logger.info("Deleting user", user_id=user_id)

    await use_case.execute(user_id)

    logger.info("User deleted", user_id=user_id)
