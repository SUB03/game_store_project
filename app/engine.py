from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("postgresql+psycopg://postgres:postgres@localhost:5432/learning", echo=True)

metadata_obj = MetaData()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

"""for ORM use cases:

class Base(DeclarativeBase):
    pass
async_session_local = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db():
    async with async_session_local() as db:
        yield db
"""