"""Create Post Use Case."""
from src.core.application.use_cases import BaseUseCase
from src.modules.posts.application.dto import CreatePostDto, PostResponseDto
from src.modules.posts.domain.entities import PostEntity
from src.modules.posts.domain.repositories import IPostRepository


class CreatePostUseCase(BaseUseCase[CreatePostDto, PostResponseDto]):
    """Use case for creating a post."""

    def __init__(self, post_repository: IPostRepository):
        self.post_repository = post_repository

    async def execute(self, input_dto: CreatePostDto) -> PostResponseDto:
        """Execute the use case."""
        # Create domain entity
        post_entity = PostEntity(
            title=input_dto.title,
            content=input_dto.content,
            user_id=input_dto.user_id,
            is_published=input_dto.is_published,
        )

        # Save via repository
        created_post = await self.post_repository.create(post_entity)

        # Convert to DTO
        return PostResponseDto(
            id=created_post.id,
            title=created_post.title,
            content=created_post.content,
            user_id=created_post.user_id,
            is_published=created_post.is_published,
            created_at=created_post.created_at,
            updated_at=created_post.updated_at,
        )
