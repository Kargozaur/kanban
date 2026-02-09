from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def sqlalchemy_handler(app: FastAPI) -> None:
    @app.exception_handler(SQLAlchemyError)
    async def sqlalch_base_handler(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": "SQLAlchemyException"})

    @app.exception_handler(IntegrityError)
    async def integrety_error(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": "Duplicate fields are not allowed for this entity"},
        )
