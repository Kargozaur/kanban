from sqlalchemy import text
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP
from datetime import datetime, timezone


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
