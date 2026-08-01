from datetime import timezone, timedelta, datetime
from typing import Annotated
import uuid

from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Cookie, Depends, HTTPException, Header, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param

from auth_service.engine import engine
from auth_service.schemas.users import UserBase, UserDB, CreateUser
from auth_service.schemas.token import Token
from .users_utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    create_tokens,
    verify_user,
    insert_user,
    get_user_from_jwt,
    get_user,
    store_token_in_db,
    delete_token_from_db,
    decode_jwt
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserBase)
async def get_users_me(user: Annotated[UserDB, Depends(get_user_from_jwt)]):
    return user

@router.post("/login")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(form_data.username)
    user = verify_user(user, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    jti = uuid.uuid4()
    access_token, refresh_token, refresh_expire = create_tokens(user.username, str(jti))
    await store_token_in_db(jti, refresh_expire)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "authorized", "CSRF": str(jti)}

@router.post("/logout")
async def logout(response: Response, refresh_token: Annotated[str | None, Cookie()] = None):
    if refresh_token: 
        _, refresh_token = get_authorization_scheme_param(refresh_token)
        payload = Token(**decode_jwt(refresh_token))
        await delete_token_from_db(payload.jti)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "logged out"}

@router.post("/refresh")
async def refresh(
        response: Response,
        csrf: Annotated[str | None, Header(alias="CSRF")] = None,
        refresh_token: Annotated[str | None, Cookie()] = None
    ):
    if not refresh_token or not csrf:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    _, refresh_token = get_authorization_scheme_param(refresh_token)
    payload = Token(**decode_jwt(refresh_token))
    if str(payload.jti) != csrf:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    await delete_token_from_db(payload.jti)

    jti = uuid.uuid4()
    access_token, refresh_token, refresh_expire = create_tokens(payload.sub, str(jti))
    await store_token_in_db(jti, refresh_expire)

    response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "authorized", "CSRF": str(jti)}

@router.post("/registrate")
async def registrate(response: Response, user_data: CreateUser):
    try:
        await insert_user(user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user with this email or username already exists"
        )
    jti = uuid.uuid4()
    access_token, refresh_token, refresh_expire = create_tokens(user_data.username, str(jti))
    await store_token_in_db(jti, refresh_expire)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "authorized", "CSRF": str(jti)}


#TODO: logout from all devices