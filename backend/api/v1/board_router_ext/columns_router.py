from fastapi import APIRouter
from backend.core.utility.role_enum import RoleEnum
from backend.dependancies.columns_dep import ColumnSvcDep
from backend.dependancies.permission_dep import PermissionDep
from backend.schemas.columns_schema import (
    ColumnCreate,
    ColumnUpdate,
    ColumnGetFull,
    ColumnGet,
)


def create_columns_router():
    columns_router = APIRouter(
        prefix="/{board_id}/columns", tags=["Board", "Columns"]
    )

    @columns_router.post(
        "/add",
        status_code=201,
        response_model=ColumnGet,
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        description="Add column to the board. Requires admin role",
    )
    async def add_column(
        board_id: int,
        column_data: ColumnCreate,
        columns_svc: ColumnSvcDep,
    ):
        return await columns_svc.add_column(
            board_id=board_id, column_data=column_data
        )

    @columns_router.get(
        "/{column_id}",
        status_code=200,
        response_model=ColumnGetFull,
        dependencies=[
            PermissionDep(
                [RoleEnum.ADMIN, RoleEnum.MEMBER, RoleEnum.VIEWER]
            )
        ],
        description="Get a full view on the column.",
    )
    async def get_column(
        column_id: int, board_id: int, columns_svc: ColumnSvcDep
    ):
        return await columns_svc.get_column_with_task(
            column_id=column_id, board_id=board_id
        )

    @columns_router.patch(
        "/{column_id}",
        status_code=200,
        response_model=ColumnGet,
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        description="Update a column. Requires admin role ",
    )
    async def update_column(
        column_id: int,
        board_id: int,
        new_column_data: ColumnUpdate,
        columns_svc: ColumnSvcDep,
    ):
        return await columns_svc.update_column(
            column_id=column_id,
            board_id=board_id,
            new_data=new_column_data,
        )

    @columns_router.delete(
        "/{column_id}",
        status_code=204,
        dependencies=[PermissionDep([RoleEnum.ADMIN])],
        description="Deletes column. Requires admin role",
    )
    async def delete_column(
        column_id: int, board_id: int, columns_svc: ColumnSvcDep
    ):
        await columns_svc.drop_column(
            column_id=column_id, board_id=board_id
        )

    return columns_router
