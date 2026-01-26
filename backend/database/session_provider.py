from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator


async def get_db(
    request: Request,
) -> AsyncIterator[AsyncSession]:
    async for session in request.app.state.db.session_generator():
        yield session
