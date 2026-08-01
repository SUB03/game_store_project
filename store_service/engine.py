from contextlib import asynccontextmanager
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

class Settings(BaseSettings):
    db_url: str = Field(alias="SQLALCHEMY_URL")

settings = Settings()

engine = create_async_engine(settings.db_url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()