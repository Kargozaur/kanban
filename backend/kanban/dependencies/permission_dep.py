from fastapi import Depends
from fastapi.params import Depends as dependencyInstance

from backend.kanban.core.security.permission_service import PermissionService
from backend.kanban.core.utility.role_enum import RoleEnum
from backend.kanban.dependencies.auth_dep import CurrentUserDep
from backend.kanban.dependencies.db_dep import DBDep


def PermissionDep(required_roles: list[RoleEnum] | RoleEnum) -> dependencyInstance:
    """
    Permission dependency for the requests, related to the endpoints. \n
    Manages BoardMembers table. Checks the of the user inside the table.
    It is managed inside the router like this : \n
    @router.put("/", dependencies=[PermissionDep(RoleEnum.ADMIN)])
    """
    if not isinstance(required_roles, list):
        required_roles = [required_roles]

    async def permission_checker(
        board_id: int, user: CurrentUserDep, session: DBDep
    ) -> bool:
        permission_service = PermissionService(session)
        await permission_service.check_user_board_role(
            user.id, board_id, required_roles
        )
        return True

    return Depends(permission_checker)
