from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[
    ModelT,
    CreateSchemaT: BaseModel,
    UpdateSchemaT: BaseModel = None,
]:
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get_entity(self, **filters: object) -> ModelT | None:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: CreateSchemaT, **extra_fields: object) -> ModelT:
        payload: dict[str, Any] = data.model_dump()
        payload.update(extra_fields)
        db_obj: ModelT = self.model(**payload)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update(
        self,
        data_to_update: UpdateSchemaT,
        **filters: object,
    ) -> None | ModelT:
        existing_field = await self.get_entity(**filters)
        if not (existing_field):
            return None
        update_data: dict[str, Any] = data_to_update.model_dump(
            exclude_unset=True, exclude={"id", "user_id"}
        )
        for k, v in update_data.items():
            if hasattr(existing_field, k):
                setattr(existing_field, k, v)
        await self.session.flush()
        return existing_field

    async def delete(self, **filters: object) -> None | bool:

        if not (existing_field := await self.get_entity(**filters)):
            return None
        await self.session.delete(existing_field)
        await self.session.flush()
        return True
