from enum import StrEnum


class TaskErrorKeys(StrEnum):
    CONFLICT = "Task conflict"
    CREATION_FAIL = "Creation failed"
    NOT_FOUND = "Task is not found"
    COLUMT_NOT_FOUND = "Column not found"
    BOARD_NOT_FOUND = "Board not found"
    USER_NOT_FOUND = "User not found"


class MemberErrorKeys(StrEnum):
    EMAIL = "Email"
    SELF_DEMOTE = "Self demote"
    MEMBER_PERSISTS = "Member persists"
    SECOND_ADMIN = "Second admin"
    USER_NOT_FOUND = "User not found"


class ColumnErrorKeys(StrEnum):
    NOT_FOUND = "Column not found"


class BoardErrorKeys(StrEnum):
    BASE = "Board exception"
    NOT_FOUND = "Board not found"
    PERMISSION_DENIED = "Board permission denied"


class UserErrorKeys(StrEnum):
    NOT_FOUND = "User with this credentials is not found"
    ALREADY_EXISTS = "User with this credentials already exists"
