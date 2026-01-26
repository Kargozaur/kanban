from pydantic import ValidationInfo


def set_name(name: str | None, info: ValidationInfo) -> str:
    return (
        name
        if name is not None
        else info.data.get("email").split("@", 1)[0]
    )
