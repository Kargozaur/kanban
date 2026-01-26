from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session_provider import get_db

DBDep = Annotated[AsyncSession, Depends(get_db)]
