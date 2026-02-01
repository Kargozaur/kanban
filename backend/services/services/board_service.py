from backend.core.decorators.transactional import transactional
from backend.core.decorators.read_only import read_only
from backend.database.unit_of_work import UnitOfWork
from backend.schemas.pagination_schema import Pagination
from backend.schemas.board_schema import (
    BoardCreate,
    BoardUpdate,
    BoardGet,
    BoardFullView,
)
from backend.core.exceptions.board_exceptions import (
    BoardBaseException,
    BoardNotFound,
    BoardPermissionDenied,
)
from backend.core.exceptions.members_exceptions import (
    MemberAlreadyPersists,
    EmailDoesNotExists,
    MemberNotFound,
)
from backend.schemas.member_schema import (
    AddBoardMemberEmail,
    AddBoardMemberUUID,
    UpdateBoardMember,
)
from uuid import UUID
from typing import Sequence


class BoardService:
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
    async def create_board(
        self, owner_id: UUID, board_data: BoardCreate
    ) -> BoardGet:
        if not (
            result := await self.uow.boards.create_board(
                owner_id=owner_id, board_data=board_data
            )
        ):
            raise BoardBaseException("Could not create a board")
        return BoardGet.model_validate(result)

    @read_only
    async def get_boards(
        self, user_id: UUID, pagination: Pagination
    ) -> Sequence[BoardGet]:
        result = await self.uow.boards.get_boards(
            user_id=user_id, pagination=pagination
        )
        return [BoardGet.model_validate(values) for values in result]

    @read_only
    async def get_board(
        self, user_id: UUID, id: int
    ) -> BoardFullView:
        if not (
            result := await self.uow.boards.get_board(
                user_id=user_id, id=id
            )
        ):
            raise BoardNotFound(
                f"Board with the id {id} is not found"
            )
        return BoardFullView.model_validate(result)

    @transactional
    async def update_board(
        self, board_id: int, data_to_update: BoardUpdate
    ) -> BoardGet:
        if not (
            result := await self.uow.boards.update_board(
                board_id=board_id,
                data_to_update=data_to_update,
            )
        ):
            raise BoardNotFound(
                f"Coudn't find a board with the id: {board_id}"
            )
        return BoardGet.model_validate(result)

    @transactional
    async def delete_board(self, id: int) -> str:
        result = await self.uow.boards.delete_board(id)
        if not result:
            raise BoardPermissionDenied(result["detail"])
        return f"Board {id} was succesfully deleted"

    @transactional
    async def add_member_to_the_board(
        self, board_id: int, user_data: AddBoardMemberEmail
    ) -> dict[str, str]:
        user = await self._get_user(email=user_data.email)
        new_member = AddBoardMemberUUID(
            role=user_data.role, user_id=user
        )

        if not (
            await self.uow.member.add_member(
                board_id=board_id, new_user_data=new_member
            )
        ):
            raise MemberAlreadyPersists(
                f"User with the {new_member.user_id} already persists in the board"
            )
        return {
            "message": f"succesfully added user with the email {user_data.email}"
        }

    @transactional
    async def update_user_role(
        self, board_id: int, user_email: str, role: UpdateBoardMember
    ) -> dict[str, str]:
        user = await self._get_user(email=user_email)

        if not (
            new_user_role := await self.uow.member.update_member_role(
                board_id=board_id, user_id=user, new_role=role
            )
        ):
            raise MemberNotFound(
                f"Member with the id {user} is not found in the board"
            )

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
