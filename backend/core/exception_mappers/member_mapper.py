from collections.abc import Callable

from backend.core.exceptions.members_exceptions import (
    EmailDoesNotExists,
    MemberAlreadyPersists,
    MemberNotFound,
    SecondAdmin,
    SelfDemote,
)
from backend.core.utility.exception_map_keys import MemberErrorKeys


ERROR_MAP: dict[MemberErrorKeys, Callable[[], Exception]] = {
    MemberErrorKeys.EMAIL: lambda: EmailDoesNotExists(
        "User with this email does not exists"
    ),
    MemberErrorKeys.SELF_DEMOTE: lambda: SelfDemote("You can not demote yourself"),
    MemberErrorKeys.MEMBER_PERSISTS: lambda: MemberAlreadyPersists(
        "User with this id already persists in the board"
    ),
    MemberErrorKeys.SECOND_ADMIN: lambda: SecondAdmin(
        "You can not add another admin to the board"
    ),
    MemberErrorKeys.USER_NOT_FOUND: lambda: MemberNotFound(
        "Member with this credentials is not found in the board"
    ),
}
