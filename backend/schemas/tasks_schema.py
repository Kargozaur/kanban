from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TaskView(BaseModel):
    title: str
    description: str
    position: Decimal

    model_config = ConfigDict(from_attributes=True)
