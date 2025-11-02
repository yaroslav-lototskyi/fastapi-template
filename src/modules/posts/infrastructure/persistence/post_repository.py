"""Post Repository Implementation."""
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.posts.domain.entities import PostEntity
from src.modules.posts.domain.repositories import IPostRepository
from .post_model import PostModel


class PostRepository(IPostRepository):
    """SQLAlchemy implementation of IPostRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: PostEntity) -> PostEntity:
        """Create a new post."""
        model = self._entity_to_model(entity)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def find_by_id(self, id: int) -> Optional[PostEntity]:
        """Find post by ID."""
        result = await self.session.execute(select(PostModel).where(PostModel.id == id))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None

    async def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[PostEntity], int]:
        """Find all posts with pagination."""
        count_result = await self.session.execute(select(func.count(PostModel.id)))
        total = count_result.scalar_one()

        result = await self.session.execute(
            select(PostModel).order_by(PostModel.created_at.desc()).offset(skip).limit(limit)
        )
        models = list(result.scalars().all())
        entities = [self._model_to_entity(model) for model in models]
        return entities, total

    async def update(self, id: int, entity: PostEntity) -> Optional[PostEntity]:
        """Update post."""
        result = await self.session.execute(select(PostModel).where(PostModel.id == id))
        model = result.scalar_one_or_none()

        if not model:
            return None

        model.title = entity.title
        model.content = entity.content
        model.is_published = entity.is_published

        await self.session.flush()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def delete(self, id: int) -> bool:
        """Delete post."""
        result = await self.session.execute(select(PostModel).where(PostModel.id == id))
        model = result.scalar_one_or_none()

        if not model:
            return False

        await self.session.delete(model)
        await self.session.flush()
        return True

    async def find_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[List[PostEntity], int]:
        """Find posts by user ID."""
        count_result = await self.session.execute(
            select(func.count(PostModel.id)).where(PostModel.user_id == user_id)
        )
        total = count_result.scalar_one()

        result = await self.session.execute(
            select(PostModel)
            .where(PostModel.user_id == user_id)
            .order_by(PostModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        models = list(result.scalars().all())
        entities = [self._model_to_entity(model) for model in models]
        return entities, total

    async def find_published(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[PostEntity], int]:
        """Find only published posts."""
        count_result = await self.session.execute(
            select(func.count(PostModel.id)).where(PostModel.is_published == True)
        )
        total = count_result.scalar_one()

        result = await self.session.execute(
            select(PostModel)
            .where(PostModel.is_published == True)
            .order_by(PostModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        models = list(result.scalars().all())
        entities = [self._model_to_entity(model) for model in models]
        return entities, total

    def _entity_to_model(self, entity: PostEntity) -> PostModel:
        """Convert domain entity to database model."""
        return PostModel(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            user_id=entity.user_id,
            is_published=entity.is_published,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def _model_to_entity(self, model: PostModel) -> PostEntity:
        """Convert database model to domain entity."""
        return PostEntity(
            id=model.id,
            title=model.title,
            content=model.content,
            user_id=model.user_id,
            is_published=model.is_published,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
