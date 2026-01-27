from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import String, UUID
from backend.models.camel_to_snake import camel_to_snake
from backend.models.mixins import (
    CreatedAt,
    UpdatedAt,
    OwnedBy,
    IdMixin,
)
from uuid import uuid4, UUID as uuid


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)


class User(CreatedAt, UpdatedAt, Base):
    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    boards: Mapped[list["Boards"]] = relationship(
        "Boards", back_populates="user"
    )


class Boards(IdMixin, OwnedBy, CreatedAt, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        String(200), nullable=False, default=""
    )
