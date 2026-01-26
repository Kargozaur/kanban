from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


async def get_db(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = request.app.state.db.session()
    async for session in async_session:
        yield session
