from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)
from sqlalchemy.types import String, UUID
from backend.models.camel_to_snake import camel_to_snake
from uuid import UUID as uuid


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)


class User(Base):
    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
