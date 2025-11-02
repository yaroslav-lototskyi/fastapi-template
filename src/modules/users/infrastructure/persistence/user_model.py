"""
User SQLAlchemy Model (Infrastructure Layer).

Model = database representation.
Entity = domain representation.

They are SEPARATE in Clean Architecture!
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class UserModel(Base):
    """
    SQLAlchemy model for User.

    This is infrastructure detail - belongs to infrastructure layer.
    Domain layer doesn't know about SQLAlchemy!

    Mapping:
    UserEntity (domain) <--> UserModel (database)
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email})>"
