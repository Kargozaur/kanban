from fastapi import Depends
from backend.database.uow_provider import get_uow
from backend.database.unit_of_work import UnitOfWork
from typing import Annotated

UOWDep = Annotated[UnitOfWork, Depends(get_uow)]
