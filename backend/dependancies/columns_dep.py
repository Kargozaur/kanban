from fastapi import Depends
from typing import Annotated
from backend.services.services.columns_svc import ColumnService
from backend.dependancies.uow_dep import UOWDep
from typing_extensions import Doc


def get_column_svc(uow: UOWDep) -> ColumnService:
    return ColumnService(uow)


ColumnSvcDep = Annotated[
    ColumnService,
    Depends(get_column_svc),
    Doc("Dependancy for the column service inside the board router"),
]
