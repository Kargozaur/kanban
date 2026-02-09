from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.kanban.core.utility.role_enum import RoleEnum
from backend.kanban.schemas.generic import GenericId
from backend.kanban.schemas.tasks_schema import TaskView
from backend.kanban.schemas.user_schema import UserGetForTotal


class BoardCreate(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=100,
            title="Board Name",
            description="The display name of the kanban board. "
            "Must be unique for the user",
        ),
    ]
    description: Annotated[
        str,
        Field(
            default="",
            max_length=200,
            description="Long form explonation of the board purpose",
            examples=["This board tracks the development of the new app"],
        ),
    ]


class BoardGetBase(GenericId[int]):
    name: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardGet(BoardGetBase):
    owner_id: UUID


class BoardUpdate(BaseModel):
    name: Annotated[str | None, Field(default=None, min_length=8)]
    description: Annotated[str | None, Field(default=None)]


class MemberView(BaseModel):
    role: RoleEnum
    user: UserGetForTotal

    model_config = ConfigDict(from_attributes=True)


class ColumnBoardView(BaseModel):
    name: str
    position: Decimal
    tasks: list[TaskView] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class BoardFullView(GenericId[int]):
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    board_members: Annotated[list[MemberView], Field(default_factory=list)]
    columns: Annotated[list[ColumnBoardView], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)
