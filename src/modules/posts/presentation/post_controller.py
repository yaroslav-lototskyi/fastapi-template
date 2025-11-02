"""
Post Controller - Hybrid DI Approach.

Stateless services (logger) → Singleton via container
Stateful services (DB, repository, use cases) → Per-request via Depends
"""
from fastapi import APIRouter, Depends, status

from src.modules.posts.dependencies import get_logger
from src.modules.posts.application.dto import CreatePostDto, PostResponseDto
from src.modules.posts.application.use_cases import CreatePostUseCase
from src.modules.posts.post_providers import get_create_post_use_case


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# ==========================================
# Create Post
# ==========================================


@router.post(
    "",
    response_model=PostResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
)
async def create_post(
    dto: CreatePostDto,
    # Stateful (per-request) - dependency chain via Depends
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
    # Stateless (singleton) - via container
    logger=Depends(get_logger),
):
    """
    Create new post - Hybrid DI approach.

    Stateful chain: DB → Repository → UseCase (per-request)
    Stateless: Logger (singleton)
    """
    logger.info(
        "Creating post",
        title=dto.title,
        author_id=dto.author_id,
    )

    # Execute use case - NO manual instantiation!
    post = await use_case.execute(dto)

    logger.info("Post created", post_id=post.id, title=post.title)

    return post
