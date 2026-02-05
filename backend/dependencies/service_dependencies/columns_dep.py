from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.dependencies.uow_dep import UOWDep
from backend.services.services.columns_svc import ColumnService


def get_column_svc(uow: UOWDep) -> ColumnService:
    return ColumnService(uow)


ColumnSvcDep = Annotated[
    ColumnService,
    Depends(get_column_svc),
    Doc("dependency for the column service inside the board router"),
]
