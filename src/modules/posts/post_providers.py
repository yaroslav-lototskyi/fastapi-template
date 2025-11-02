"""Post Module Providers (Dependency Injection)."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.modules.posts.domain.repositories import IPostRepository
from src.modules.posts.infrastructure.persistence import PostRepository
from src.modules.posts.application.use_cases import CreatePostUseCase


def get_post_repository(
    db: AsyncSession = Depends(get_db),
) -> IPostRepository:
    """Provide IPostRepository implementation."""
    return PostRepository(db)


def get_create_post_use_case(
    post_repository: IPostRepository = Depends(get_post_repository),
) -> CreatePostUseCase:
    """Provide CreatePostUseCase with injected dependencies."""
    return CreatePostUseCase(post_repository)
