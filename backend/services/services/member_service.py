from uuid import UUID

from backend.core.decorators.transactional import transactional
from backend.core.exception_mappers.member_mapper import ERROR_MAP
from backend.core.utility.exception_map_keys import MemberErrorKeys
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    AddBoardMemberUUID,
    MemberResponse,
    UpdateBoardMember,
    UpdateMemberWithId,
)


class MemberService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def _get_user(self, email: str) -> UUID:
        if not (user := await self.uow.users.get_user_by_email(email=email)):
            raise ERROR_MAP[MemberErrorKeys.EMAIL]()
        return user.id

    @transactional
    async def add_member_to_the_board(
        self, board_id: int, user_data: AddBoardMemberEmail
    ) -> MemberResponse:
        user = await self._get_user(email=user_data.email)
        new_member = AddBoardMemberUUID(role=user_data.role, user_id=user)

        if not (
            result := await self.uow.member.add_member(
                board_id=board_id, new_user_data=new_member
            )
        ):
            raise ERROR_MAP[MemberErrorKeys.MEMBER_PERSISTS]()
        if result == "conflict":
            raise ERROR_MAP[MemberErrorKeys.SECOND_ADMIN]()
        message: dict[str, str] = {
            "message": f"Succesfully added user with the email {user_data.email}"
        }
        return MemberResponse.model_validate(message)

    @transactional
    async def update_user_role(
        self,
        board_id: int,
        current_user: UUID,
        user_data: UpdateBoardMember,
    ) -> MemberResponse:
        user = await self._get_user(email=user_data.email)
        if user == current_user and user_data.role != "admin":
            raise ERROR_MAP[MemberErrorKeys.SELF_DEMOTE]()
        model = UpdateMemberWithId(id=board_id, user_id=user, role=user_data.role)
        if not (result := await self.uow.member.update_member_role(member_data=model)):
            raise ERROR_MAP[MemberErrorKeys.USER_NOT_FOUND]()
        if result == "conflict":
            raise ERROR_MAP[MemberErrorKeys.SECOND_ADMIN]()
        message: dict[str, str] = {
            "message": f"Succesfully updated user role for the user {user_data.email}"
        }
        return MemberResponse.model_validate(message)

    @transactional
    async def delete_user_from_the_board(
        self, board_id: int, user_email: str, current_user: UUID
    ) -> MemberResponse:
        user = await self._get_user(user_email)

        if not (
            result := await self.uow.member.delete_member_from_the_board(
                board_id=board_id, user_id=user, current_user=current_user
            )
        ):
            raise ERROR_MAP[MemberErrorKeys.USER_NOT_FOUND]()
        if result in ["conflict", "last admin"]:
            raise ERROR_MAP[MemberErrorKeys.SECOND_ADMIN]()
        message: dict[str, str] = {"message": "Succesfully deleted user from the board"}
        return MemberResponse.model_validate(message)
