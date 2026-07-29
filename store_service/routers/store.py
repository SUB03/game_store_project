from typing import Optional
from pydantic import BaseModel

from fastapi import HTTPException, routing, Depends
from store_service.engine import engine
from store_service.models.models import games

router = routing.APIRouter(
    prefix="/store",
    tags=["store"]
)

@router.get("/games")
async def get_games(page: int = 1, per_page: int = 10):
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="page and per_page must be >= 1")
    
    async with engine.begin() as conn:
        result = await conn.execute(games.select().limit(per_page).offset(page - 1) * per_page)
        result = result.mappings().all()
    return result