from collections.abc import Callable

from backend.core.exceptions.exceptions import (
    NotFoundError,
    UserAlreadyExists,
)
from backend.core.utility.exception_map_keys import UserErrorKeys


ERROR_MAP: dict[UserErrorKeys, Callable[[], Exception]] = {
    UserErrorKeys.ALREADY_EXISTS: lambda: UserAlreadyExists(),
    UserErrorKeys.NOT_FOUND: lambda: NotFoundError(),
}
