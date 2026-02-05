from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.database.unit_of_work import UnitOfWork
from backend.database.uow_provider import get_uow


UOWDep = Annotated[
    UnitOfWork,
    Depends(get_uow),
    Doc("Annotated dependancy of the UoW. Used to initialize a service dependancies"),
]
