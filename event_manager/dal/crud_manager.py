from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        try:
            db_obj = self.model(
                **obj_in.model_dump(exclude_unset=True, exclude_none=True)
            )
            db.add(db_obj)
            await db.flush()  # Use flush instead of commit to save changes but keep the transaction open
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            print(e)
            raise e

    async def update(
        self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.flush()  # Use flush instead of commit to save changes but keep the transaction open
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> None:
        await db.execute(delete(self.model).where(self.model.id == id))
        await db.flush()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        additional_where_clause: list[Any] | None = None,
    ) -> List[ModelType]:
        query = select(self.model)

        if additional_where_clause:
            query = query.where(and_(*additional_where_clause))
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)

        result = await db.execute(query)
        return result.scalars().all()
