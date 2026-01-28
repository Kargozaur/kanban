from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Annotated
from backend.core.utility.role_enum import RoleEnum


class BoardCreate(BaseModel):
    name: str = Field(default=..., min_length=8)
    description: str = Field(default="")


class BoardGet(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    owned_id: UUID

    model_config = ConfigDict(from_attributes=True)


class BoardUpdate(BaseModel):
    name: Optional[Annotated[str, Field(..., min_length=8)]] = None
    description: Optional[str] = None


class User(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class MemberView(BaseModel):
    user_id: UUID
    role: RoleEnum
    user: User

    model_config = ConfigDict(from_attributes=True)


class TaskBoardView(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ColumnBoardView(BaseModel):
    id: int
    name: str
    orders: int
    tasks: list[TaskBoardView] = []


class BoardFullView(BaseModel):
    id: int
    name: str
    description: str
    owned_id: UUID
    created_at: datetime

    board_members: list[MemberView] = Field(default_factory=list)
    columns: list[ColumnBoardView] = Field(default_factory=list)
