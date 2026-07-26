from datetime import timezone, timedelta, datetime
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncEngine

from app.utils.oauth_with_cookies import OAuth2PasswordBearerWithCookie
from app.engine import engine
from app.models.users import users_table
from app.schemas.users import UserBase, UserDB
from app.utils.hash_password import (
    get_password_hash,
    verify_password,
    verify_dummy, 
    SECRET_KEY,
    ALGORITHM
)

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 31 * 24 * 60 

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="users/login")

def verify_user(user: UserDB, password: str):
    if not user:
        verify_dummy(password)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_jwt_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_user_from_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exeption
    except InvalidTokenError:
        raise credentials_exeption
    user = await get_user(engine, username)
    if user is None:
        raise credentials_exeption
    return user


async def get_user(engine: AsyncEngine, username: str) -> UserDB:
    async with engine.begin() as conn:
        result = await conn.execute(
            users_table.select().where(users_table.c.username == username)
        )
        result = result.fetchone()
        if not result:
            return None
        return UserDB(**result._asdict())

@router.get("/me", response_model=UserBase)
async def get_users_me(user: Annotated[UserDB, Depends(get_user_from_jwt)]):
    return user

@router.post("/login")
async def login(respone: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(engine, form_data.username)
    user = verify_user(user, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token({"sub": user.username}, access_token_expires)
    refresh_token = create_jwt_token({"sub": user.username}, refresh_token_expires)

    respone.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    respone.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message", "authorized"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "logged out"}