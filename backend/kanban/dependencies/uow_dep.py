from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.kanban.database.unit_of_work import UnitOfWork
from backend.kanban.database.uow_provider import get_uow


UOWDep = Annotated[
    UnitOfWork,
    Depends(get_uow),
    Doc("Annotated dependency of the UoW. Used to initialize a service dependencies"),
]
