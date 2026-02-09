from __future__ import annotations

from decimal import Decimal
from uuid import UUID as uuid, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
    synonym,
)
from sqlalchemy.types import DECIMAL, UUID, String

from backend.kanban.core.utility.role_enum import RoleEnum
from backend.kanban.models.camel_to_snake import camel_to_snake
from backend.kanban.models.mixins import (
    CreatedAt,
    IdMixin,
    OwnedBy,
    UpdatedAt,
)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


class User(CreatedAt, UpdatedAt, Base):
    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    boards: Mapped[list[Boards]] = relationship("Boards", back_populates="user")
    board_members: Mapped[list[BoardMembers]] = relationship(
        "BoardMembers",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    tasks: Mapped[list[Tasks]] = relationship(
        "Tasks", back_populates="user", foreign_keys="[Tasks.owner_id]"
    )
    assigned_task: Mapped[list[Tasks]] = relationship(
        "Tasks", back_populates="assignee", foreign_keys="[Tasks.assignee_id]"
    )


class Boards(IdMixin, OwnedBy, CreatedAt, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    board_members: Mapped[list[BoardMembers]] = relationship(
        "BoardMembers",
        back_populates="boards",
        cascade="all, delete-orphan",
    )
    columns: Mapped[list[Columns]] = relationship(
        "Columns",
        back_populates="boards",
        cascade="all, delete-orphan",
    )

    tasks: Mapped[list[Tasks]] = relationship(
        "Tasks", back_populates="boards", cascade="all, delete-orphan"
    )


class BoardMembers(Base):
    """OwnedBy mixin isn't used due to the possibility of the large
    amount of write/insert/delete operations.\n"""

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    )
    user_id: Mapped[uuid] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[RoleEnum] = mapped_column(nullable=False)
    boards: Mapped[Boards] = relationship("Boards", back_populates="board_members")
    user: Mapped[User] = relationship("User", back_populates="board_members")

    __table_args__ = (
        UniqueConstraint("board_id", "user_id", name="uq_member_per_board"),
    )

    id: Mapped[int] = synonym("board_id")


class Columns(IdMixin, Base):
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100))
    position: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    wip_limit: Mapped[int] = mapped_column(nullable=True)

    boards: Mapped[Boards] = relationship("Boards", back_populates="columns")
    tasks: Mapped[list[Tasks]] = relationship(
        "Tasks",
        order_by="Tasks.position",
        back_populates="columns",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("board_id", "name", name="uq_column_name_per_board"),
        UniqueConstraint(
            "board_id",
            "position",
            name="uq_column_position_per_board",
        ),
    )


class Tasks(IdMixin, OwnedBy, CreatedAt, Base):
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id", ondelete="CASCADE"))
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id: Mapped[uuid | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    description: Mapped[str] = mapped_column(
        String(200),
    )
    position: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    columns: Mapped[Columns] = relationship("Columns", back_populates="tasks")
    assignee: Mapped[User] = relationship(
        "User",
        foreign_keys=[assignee_id],
        back_populates="assigned_task",
    )
    boards: Mapped[Boards] = relationship(
        "Boards", back_populates="tasks", foreign_keys=[board_id]
    )

    user: Mapped[User] = relationship(
        "User", back_populates="tasks", foreign_keys="[Tasks.owner_id]"
    )
