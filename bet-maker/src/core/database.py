import logging
from decimal import Decimal
from typing import AsyncGenerator

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, sessionmaker

from .config import Config

logger = logging.getLogger("DATABASE")
engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class AbstractBase(Base):
    __abstract__ = True

    @classmethod
    def primary_keys(cls) -> list[Mapped]:
        return [getattr(cls, item.key) for item in inspect(cls).primary_key]


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_db_and_tables(tables: list[AbstractBase]):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_bets(db):
    async with async_session() as session:
        bets = [
            db(event_id=f"{i}", bet_amount=Decimal(100.0 + i * 10))
            for i in range(1, 10)
        ]

        session.add_all(bets)
        await session.commit()
