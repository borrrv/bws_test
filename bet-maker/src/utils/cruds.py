import logging

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import AbstractResponseModel, AbstractTable

logger = logging.getLogger(__name__)


class GetOneService(AbstractTable, AbstractResponseModel):
    @classmethod
    async def get_one(
        cls, session: AsyncSession, _id: any, jinja: bool = False
    ) -> BaseModel:
        instance = await session.get(cls.table, _id)
        if not instance:
            logger.error("Not result found")
            raise HTTPException(status_code=404, detail="Not result found")
        return instance if jinja else cls.response_model.model_validate(instance)


class GetListService(AbstractTable, AbstractResponseModel):

    @classmethod
    async def get_list(
        cls, session: AsyncSession, query=None, limit: int = 10, offset: int = 0
    ) -> list[BaseModel]:
        if query is None:
            query = (
                select(cls.table)
                .order_by(cls.table.id.desc())
                .limit(limit)
                .offset(offset)
            )
        query_result = (await session.execute(query)).scalars().all()
        if not query_result:
            return []
        _list = [cls.response_model.model_validate(item) for item in query_result]
        return _list

    @classmethod
    async def get_total_count(cls, session: AsyncSession) -> str:
        query = select(func.count(cls.table.primary_keys()[0]))
        query_result = (await session.execute(query)).scalars().first()
        return str(query_result)


class CreateService(AbstractTable, AbstractResponseModel):
    @classmethod
    async def create_one(cls, session: AsyncSession, params: BaseModel) -> BaseModel:
        instance = cls.table(**params.model_dump(exclude_none=True))
        session.add(instance)
        await session.commit()
        logger.warning("Creation was successful")
        return cls.response_model.model_validate(instance)


class UpdateService(AbstractTable):
    @classmethod
    async def update_one(
        cls,
        session: AsyncSession,
        _id: any,
        params: BaseModel,
        exclude_fields: set = set(),
    ):
        instance = await session.get(cls.table, _id)
        if not instance:
            raise HTTPException(status_code=404, detail="Not result found")
        query = (
            update(cls.table)
            .where(cls.table.primary_keys()[0] == _id)
            .values(params.model_dump(exclude=exclude_fields, exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()


class DeleteService(AbstractTable):
    @classmethod
    async def delete_one(cls, session: AsyncSession, _id: any):
        instance = await session.get(cls.table, _id)
        if not instance:
            raise HTTPException(status_code=404, detail="Not result found")
        await session.delete(instance)
        await session.commit()

    @classmethod
    async def delete_many(cls, session: AsyncSession, condition):
        query = delete(cls.table).where(condition)
        await session.execute(query)
        await session.commit()
