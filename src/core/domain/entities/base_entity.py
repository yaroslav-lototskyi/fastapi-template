"""
Base Entity for Domain Layer (Clean Architecture).

Provides common fields and behavior for all domain entities.
"""
from datetime import datetime
from typing import Optional


class BaseEntity:
    """
    Base domain entity.
    Contains common fields for all entities.

    In Clean Architecture:
    - Entities are business objects with identity
    - They contain business logic (methods)
    - They are framework-agnostic (no SQLAlchemy here!)
    """

    id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __init__(
        self,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    def __eq__(self, other) -> bool:
        """Entities are equal if they have the same ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
