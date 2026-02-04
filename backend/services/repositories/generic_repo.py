from typing import Any
from uuid import UUID

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
        request_user: UUID | None = None,
        **filters: object,
    ) -> None | ModelT:
        query = select(self.model).filter_by(**filters)
        existing_field = await self.session.execute(query)
        if not (current_object := existing_field.scalar_one_or_none()):
            return None
        update_data: dict[str, Any] = data_to_update.model_dump(
            exclude_unset=True, exclude={"id", "user_id"}
        )
        if request_user and current_object.id == request_user:
            update_data.pop("is_admin", None)
            update_data.pop("is_superuser", None)
        for k, v in update_data.items():
            if hasattr(current_object, k):
                setattr(current_object, k, v)
        await self.session.flush()
        return current_object

    async def delete(
        self, request_user: UUID | None = None, **filters: object
    ) -> None | bool:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        existing_field = result.scalar_one_or_none()
        if not existing_field:
            return None
        if request_user and existing_field.owner_id == request_user:
            return None
        await self.session.delete(existing_field)
        await self.session.flush()
        return True
