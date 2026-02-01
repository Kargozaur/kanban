from backend.services.services.member_service import MemberService
from backend.dependancies.uow_dep import UOWDep


def get_member_svc(uow: UOWDep) -> MemberService:
    return MemberService(uow)
