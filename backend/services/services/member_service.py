from backend.core.decorators.transactional import transactional
from backend.database.unit_of_work import UnitOfWork
from backend.core.exceptions.members_exceptions import (
    MemberAlreadyPersists,
    EmailDoesNotExists,
)
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    AddBoardMemberUUID,
    UpdateBoardMember,
)
from backend.core.exceptions.members_exceptions import (
    MemberNotFound,
)
from uuid import UUID


class MemberService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def _get_user(self, email: str) -> UUID:
        if not (
            user := await self.uow.users.get_user_by_email(
                email=email
            )
        ):
            raise EmailDoesNotExists(f"{email} does not exists")
        return user.id

    @transactional
    async def add_member_to_the_board(
        self, board_id: int, user_data: AddBoardMemberEmail
    ) -> dict[str, str]:
        user = await self._get_user(email=user_data.email)
        new_member = AddBoardMemberUUID(
            role=user_data.role, user_id=user
        )

        if not (
            result := await self.uow.member.add_member(
                board_id=board_id, new_user_data=new_member
            )
        ):
            raise MemberAlreadyPersists(
                f"User with the {new_member.user_id} already persists in the board"
            )
        if result == "conflict":
            return {
                "message": "You can not add another admin for the board"
            }
        return {
            "message": f"succesfully added user with the email {user_data.email}"
        }

    @transactional
    async def update_user_role(
        self, board_id: int, user_email: str, role: UpdateBoardMember
    ) -> dict[str, str]:
        user = await self._get_user(email=user_email)

        if not (
            result := await self.uow.member.update_member_role(
                board_id=board_id, user_id=user, new_role=role
            )
        ):
            raise MemberNotFound(
                f"Member with the id {user} is not found in the board"
            )
        if result == "conflict":
            return {"message": "You can not set user role as admin"}
        return {
            "message": f"Succesfully updated user role for the user {user_email}"
        }

    @transactional
    async def delete_user_from_the_board(
        self, board_id: int, user_email: str
    ) -> dict[str, str]:
        user = await self._get_user(user_email)

        if not (
            await self.uow.member.delete_member_from_the_board(
                board_id=board_id, user_id=user
            )
        ):
            raise MemberNotFound(
                f"Member with the id {user_email} is not found in the board"
            )
        return {"message": "Succesfully deleted user from the board"}
