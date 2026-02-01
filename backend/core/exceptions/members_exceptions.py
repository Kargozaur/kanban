class MemberBaseException(Exception):
    status_code = 500
    detail = "Member base exception"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self) -> str:
        return f"{self.message}"


class MemberAlreadyPersists(MemberBaseException):
    status_code = 409
    detail = "User with this email already persists in the board"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmailDoesNotExists(MemberBaseException):
    status_code = 404
    detail = "User with this email is not found"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class MemberNotFound(MemberBaseException):
    status_code = 404
    detail = "User with this id doesn't persists in the board"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class SecondAdmin(MemberBaseException):
    status_code = 409
    detail = "You can not add another user with the admin role"

    def __init__(self, message: str) -> None:
        super().__init__(message)
