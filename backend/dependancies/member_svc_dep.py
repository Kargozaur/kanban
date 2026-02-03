from fastapi import Depends
from backend.services.services.member_service import MemberService
from backend.dependancies.uow_dep import UOWDep
from typing import Annotated
from typing_extensions import Doc


def get_member_svc(uow: UOWDep) -> MemberService:
    return MemberService(uow)


MemberSvcDep = Annotated[
    MemberService,
    Depends(get_member_svc),
    Doc("Dependancy for the member service inside the border router"),
]
