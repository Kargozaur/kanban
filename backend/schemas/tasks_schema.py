from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class TaskView(BaseModel):
    title: str
    description: str
    position: Decimal

    model_config = ConfigDict(from_attributes=True)
