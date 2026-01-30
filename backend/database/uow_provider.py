from fastapi import Request
from backend.database.unit_of_work import UnitOfWork
from typing import AsyncIterator


async def get_uow(request: Request) -> AsyncIterator[UnitOfWork]:
    async for session in request.app.state.db.session_generator():
        yield UnitOfWork(session)
