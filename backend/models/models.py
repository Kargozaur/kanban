from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from uuid import uuid4, UUID as uuid
from sqlalchemy.types import String, UUID
from backend.models.camel_to_snake import camel_to_snake
from backend.core.utility.role_enum import RoleEnum
from backend.models.mixins import (
    CreatedAt,
    UpdatedAt,
    OwnedBy,
    IdMixin,
)


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
    board_members: Mapped[list["BoardMembers"]] = relationship(
        "BoardMembers",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Boards(IdMixin, OwnedBy, CreatedAt, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        String(200), nullable=False, default=""
    )
    board_members: Mapped[list["BoardMembers"]] = relationship(
        "BoardMembers",
        back_populates="boards",
        cascade="all, delete-orphan",
    )


class BoardMembers(IdMixin, Base):
    """OwnedBy mixin isn't used to the possibility of the large amount of write/insert/delete operations.\n"""

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"),
        unique=True,
        index=True,
        primary_key=True,
    )
    user_id: Mapped[uuid] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    role: Mapped[RoleEnum] = mapped_column(nullable=False)
    boards: Mapped["Boards"] = relationship(
        "Boards", back_populates="board_members"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="board_members"
    )
