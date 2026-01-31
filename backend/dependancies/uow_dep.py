from fastapi import Depends
from backend.database.uow_provider import get_uow
from backend.database.unit_of_work import UnitOfWork
from typing import Annotated
from typing_extensions import Doc

UOWDep = Annotated[
    UnitOfWork,
    Depends(get_uow),
    Doc("Annotated dependancy of the UoW"),
]
