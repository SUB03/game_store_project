from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+psycopg://postgres:postgres@postgres:5432/learning")

metadata_obj = MetaData()