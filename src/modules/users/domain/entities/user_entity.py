"""
User Domain Entity (Clean Architecture).

Domain entity != Database model!
- Entity = business object with identity and behavior
- Model = database representation

In Clean Architecture:
- Entity contains business logic and rules
- Separate from database implementation details
"""
from typing import Optional
from src.core.domain.entities import BaseEntity


class UserEntity(BaseEntity):
    """
    User domain entity.

    Contains:
    - Business data
    - Business logic (methods)
    - Validation rules

    Does NOT contain:
    - Database details (no SQLAlchemy)
    - Framework details (no FastAPI)
    """

    def __init__(
        self,
        email: str,
        username: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        **kwargs,  # For base entity fields (id, created_at, etc.)
    ):
        super().__init__(**kwargs)
        self.email = email
        self.username = username
        self.full_name = full_name
        self.is_active = is_active

    def deactivate(self) -> None:
        """Business logic: deactivate user."""
        self.is_active = False

    def activate(self) -> None:
        """Business logic: activate user."""
        self.is_active = True

    def update_profile(self, full_name: Optional[str] = None) -> None:
        """Business logic: update user profile."""
        if full_name is not None:
            self.full_name = full_name

    def can_login(self) -> bool:
        """Business rule: user can login only if active."""
        return self.is_active

    def __repr__(self) -> str:
        return f"UserEntity(id={self.id}, email={self.email}, username={self.username})"
