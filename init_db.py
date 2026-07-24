import asyncio

from app.engine import engine, metadata_obj
import app.models.users

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())  