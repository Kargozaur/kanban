from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.kanban.schemas.generic import GenericId


class TaskView(GenericId[int]):
    title: str
    description: str
    position: Decimal
    created_at: datetime
    assignee_id: UUID | None

    model_config = ConfigDict(from_attributes=True)


class CreateTaskBase(BaseModel):
    title: Annotated[
        str, Field(..., min_length=1, max_length=70, examples=["Add test"])
    ]
    description: Annotated[
        str | None,
        Field(..., min_length=1, max_length=200, examples=["Description to the test"]),
    ]
    position: Annotated[
        Decimal | None,
        Field(..., gt=0, max_digits=20, decimal_places=10),
    ]


class CreateTask(CreateTaskBase):
    assignee_id: Annotated[
        UUID | None,
        Field(
            ...,
            description="assign task to the user represented in the board or skip"
            "the assignment",
        ),
    ]


class UpdateTaskBase(BaseModel):
    title: Annotated[
        str | None,
        Field(
            default=None, min_length=1, max_length=70, examples=["New name of the test"]
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=200,
            examples=["Very new name of the test"],
        ),
    ]
    position: Annotated[
        Decimal | None, Field(default=None, gt=0, max_digits=20, decimal_places=10)
    ]


class UpdateTask(UpdateTaskBase):
    assignee_id: Annotated[
        UUID | None,
        Field(
            default=None,
            description="assign task to the user represented in the board or skip",
        ),
    ]


class MoveTask(BaseModel):
    target_column_id: int
    above_task_id: int | None = None
    below_task_id: int | None = None
