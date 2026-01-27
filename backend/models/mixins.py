from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import TIMESTAMP, UUID
from datetime import datetime, timezone
from uuid import UUID as uuid


class CreatedAt:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
        server_default=text("now()"),
    )


class UpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
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
    def user(cls) -> Mapped["User | None"]:  # noqa: F821
        return relationship(
            "User", back_populates=f"{cls.__tablename__}"
        )


class IdMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
