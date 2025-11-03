"""
User List Criteria Value Object (Domain Layer).

Encapsulates business rules for listing users.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SortField(str, Enum):
    """Available fields for sorting users."""

    CREATED_AT = "created_at"
    EMAIL = "email"
    USERNAME = "username"


class SortOrder(str, Enum):
    """Sort order direction."""

    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class UserListCriteria:
    """
    Criteria for listing users (Domain Layer).

    Contains business rules for pagination and sorting.
    This is a Value Object - immutable and contains business logic.
    """

    page: int = 1
    page_size: int = 100  # Business rule: default 100 per page
    sort_field: SortField = SortField.CREATED_AT  # Business rule: sort by created_at
    sort_order: SortOrder = SortOrder.DESC  # Business rule: newest first

    # Business rules validation
    MAX_PAGE_SIZE = 1000  # Business rule: maximum items per page

    def __post_init__(self):
        """Validate business rules."""
        if self.page < 1:
            raise ValueError("Page must be >= 1")

        if self.page_size < 1:
            raise ValueError("Page size must be >= 1")

        if self.page_size > self.MAX_PAGE_SIZE:
            raise ValueError(f"Page size cannot exceed {self.MAX_PAGE_SIZE}")

    @property
    def skip(self) -> int:
        """Calculate offset for pagination (derived from page and page_size)."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit for pagination."""
        return self.page_size
