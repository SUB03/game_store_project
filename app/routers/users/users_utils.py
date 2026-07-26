from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from uuid import UUID
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import Depends, HTTPException, status

from app.engine import engine
from app.models.users import users_table, token_whitelist
from app.schemas.users import UserDB
from app.utils.hash_password import (
    get_password_hash,
    verify_password,
    verify_dummy, 
    SECRET_KEY,
    ALGORITHM
)
from app.utils.oauth_with_cookies import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="users/login")

def verify_user(user: UserDB, password: str):
    if not user:
        verify_dummy(password)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def delete_token_from_db(uuid: UUID):
    async with engine.begin() as conn:
        await conn.execute(token_whitelist.delete().where(token_whitelist.c.uid == uuid))

async def get_token_from_db(uuid: UUID):
    ...

async def store_token_in_db(uuid: UUID, expiration_date: datetime):
    async with engine.begin() as conn:
        await conn.execute(token_whitelist.insert().values(uid=uuid, expiration_at=expiration_date))

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exeption
    except ExpiredSignatureError:
        raise credentials_exeption
    return payload

async def get_user_from_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_jwt(token)
    username = payload.get("sub")
    if not username:
        raise credentials_exeption
    user = await get_user(username)
    if user is None:
        raise credentials_exeption
    return user


async def get_user(username: str) -> UserDB:
    async with engine.begin() as conn:
        result = await conn.execute(
            users_table.select().where(users_table.c.username == username)
        )
        result = result.fetchone()
        if not result:
            return None
        return UserDB(**result._asdict())