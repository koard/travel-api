import asyncio
from typing import AsyncIterator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .province_model import *
from .user_model import *

from .. import config

engine: AsyncEngine = None


async def init_db():
    global engine
    settings = config.get_settings()
    engine = create_async_engine(settings.SQLDB_URL, echo=True, future=True)
    await create_db_and_tables()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    if engine is None:
        raise Exception("Database engine not initialized.")
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session


async def close_db():
    global engine
    if engine:
        await engine.dispose()
        engine = None
