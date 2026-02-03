from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.core.exceptions.members_exceptions import (
    EmailDoesNotExists,
    MemberAlreadyPersists,
    MemberBaseException,
    MemberNotFound,
    SecondAdmin,
)


def member_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(MemberBaseException)
    async def member_base_error(
        request: Request, exc: MemberBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(MemberAlreadyPersists)
    async def member_persists_error(
        request: Request, exc: MemberAlreadyPersists
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(MemberNotFound)
    async def member_not_found_error(
        request: Request, exc: MemberNotFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(EmailDoesNotExists)
    async def email_does_not_exists_error(
        request: Request, exc: EmailDoesNotExists
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(SecondAdmin)
    async def second_admin_error(request: Request, exc: SecondAdmin) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
