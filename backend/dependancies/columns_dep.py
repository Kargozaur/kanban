from fastapi import Depends
from typing import Annotated
from backend.services.services.columns_svc import ColumnService
from backend.dependancies.uow_dep import UOWDep


def get_column_svc(uow: UOWDep) -> ColumnService:
    return ColumnService(uow)


ColumnSvcDep = Annotated[ColumnService, Depends(get_column_svc)]
