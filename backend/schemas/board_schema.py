from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Annotated
from backend.core.utility.role_enum import RoleEnum
from backend.schemas.user_schema import UserGet


class BoardCreate(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=100,
            title="Board Name",
            description="The display name of the kanban board. must be unique for the user",
        ),
    ]
    description: Annotated[
        str,
        Field(
            default="",
            max_length=200,
            description="Long form explonation of the board purpose",
            examples=[
                "This board tracks the development of the new app"
            ],
        ),
    ]


class BoardGetBase(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardGet(BoardGetBase):
    owner_id: UUID


class BoardUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, min_length=8)]
    description: Annotated[Optional[str], Field(default=None)]


class MemberView(BaseModel):
    user_id: UUID
    role: RoleEnum
    user: UserGet

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
    tasks: list[TaskBoardView] = Field(default=list)


class BoardFullView(BaseModel):
    id: int
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    board_members: Annotated[
        list[MemberView], Field(default_factory=list)
    ]
    columns: Annotated[
        list[ColumnBoardView], Field(default_factory=list)
    ]

    model_config = ConfigDict(from_attributes=True)
