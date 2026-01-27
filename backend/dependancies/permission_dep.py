from fastapi import Depends
from backend.core.security.permission_service import PermissionService
from backend.core.utility.role_enum import RoleEnum
from backend.dependancies.db_dep import DBDep
from backend.dependancies.auth_dep import CurrentUserDep


def PermissionDep(required_roles: list[RoleEnum]):
    async def permission_checker(
        board_id: int, user: CurrentUserDep, session: DBDep
    ):
        permission_service = PermissionService(session)
        await permission_service.chech_user_board_role(
            user.id, board_id, required_roles
        )
        return True

    return Depends(permission_checker)
