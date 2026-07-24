from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncEngine

from app.engine import engine
from app.models.users import users_table
from app.schemas.users import UserBase, UserDB

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def fake_hash(password: str):
    return "hash_" + password

async def get_user(engine: AsyncEngine, username: str) -> UserDB:
    async with engine.begin() as conn:
        result = await conn.execute(
            users_table.select().where(users_table.c.username == username)
        )
        result = result.fetchone()
        if not result:
            return None
        print("log", result._asdict())
        return UserDB(**result._asdict())

@router.get("/me", response_model=UserBase)
async def get_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_user(engine, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(engine, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}