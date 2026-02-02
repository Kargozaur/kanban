from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from decimal import Decimal
from backend.schemas.tasks_schema import TaskView


class ColumnCreate(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=100,
            examples=["my amazing column"],
        ),
    ]
    position: Annotated[
        Decimal | None,
        Field(
            default=None,
            gt=0,
            max_digits=20,
            decimal_places=10,
            examples=["1.0", "1.5"],
        ),
    ]
    wip_limit: Annotated[
        int | None, Field(default=None, ge=1, examples=[1, 2])
    ]


class ColumnUpdate(BaseModel):
    name: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=100,
            examples=["my new amazing column name"],
        ),
    ]
    position: Annotated[
        Decimal | None,
        Field(
            default=None,
            gt=0,
            max_digits=20,
            decimal_places=10,
            examples=["1.0", "2.0"],
        ),
    ]

    wip_limit: Annotated[
        int | None, Field(default=None, ge=1, examples=[1])
    ]


class ColumnGet(BaseModel):
    name: str
    position: Decimal
    wip_limit: int | None

    model_config = ConfigDict(from_attributes=True)


class ColumnGetFull(ColumnGet):
    tasks: list[TaskView]
