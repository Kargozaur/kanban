from typing import Annotated

from fastapi import Depends
from typing_extensions import Doc

from backend.dependancies.uow_dep import UOWDep
from backend.services.services.member_service import MemberService


def get_member_svc(uow: UOWDep) -> MemberService:
    return MemberService(uow)


MemberSvcDep = Annotated[
    MemberService,
    Depends(get_member_svc),
    Doc("Dependancy for the member service inside the border router"),
]
