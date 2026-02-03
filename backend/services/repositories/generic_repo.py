from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Any


class BaseRepository[
    ModelT,
    CreateSchemaT: BaseModel,
    UpdateSchemaT: BaseModel = None,
]:
    def __init__(
        self, session: AsyncSession, model: type[ModelT]
    ) -> None:
        self.session = session
        self.model = model

    async def create(
        self, data: CreateSchemaT, **extra_fields: Any
    ) -> ModelT:
        payload: dict[str, Any] = data.model_dump()
        payload.update(extra_fields)
        db_obj: ModelT = self.model(**payload)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update(
        self, data_to_update: UpdateSchemaT, **filters: Any
    ) -> None | ModelT:
        query = select(self.model).filter_by(**filters)
        existing_field = await self.session.execute(query)
        if not (
            current_object := existing_field.scalar_one_or_none()
        ):
            return None
        update_data: dict[str, Any] = data_to_update.model_dump(
            exclude_unset=True, exclude={"id", "user_id"}
        )
        for k, v in update_data.items():
            if hasattr(current_object, k):
                setattr(current_object, k, v)
        await self.session.flush()
        return current_object

    async def delete(self, **composite_key: Any) -> None | bool:
        query = select(self.model).filter_by(**composite_key)
        result = await self.session.execute(query)
        existing_field = result.scalar_one_or_none()
        if not existing_field:
            return None
        await self.session.delete(existing_field)
        await self.session.flush()
        return True
