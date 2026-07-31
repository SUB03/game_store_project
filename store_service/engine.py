from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+psycopg://postgres:postgres@localhost:5432/learning", echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()