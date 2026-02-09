from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.kanban.dependencies.uow_dep import UOWDep
from backend.kanban.services.services.member_service import MemberService


def get_member_svc(uow: UOWDep) -> MemberService:
    return MemberService(uow)


MemberSvcDep = Annotated[
    MemberService,
    Depends(get_member_svc),
    Doc("dependency for the member service inside the border router"),
]
