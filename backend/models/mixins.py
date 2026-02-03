from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID as uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)
from sqlalchemy.types import TIMESTAMP, UUID


class CreatedAt:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=UTC),
        server_default=text("now()"),
    )


class UpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=UTC),
        server_default=text("now()"),
    )


class OwnedBy:
    @declared_attr
    def owner_id(cls) -> Mapped[uuid | None]:
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("user.id", ondelete="CASCADE"),
            index=True,
        )

    @declared_attr
    @classmethod
    def user(cls) -> Mapped["User | None"]:  # type: ignore  # noqa: F821, UP037
        return relationship("User", back_populates=f"{cls.__tablename__}")  # ty:ignore[unresolved-attribute]


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
