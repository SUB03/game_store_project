from datetime import timezone, timedelta, datetime
from typing import Annotated
import uuid

from fastapi import APIRouter, Cookie, Depends, HTTPException, Header, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param

from auth_service.engine import engine
from auth_service.schemas.users import UserBase, UserDB
from auth_service.schemas.token import Token
from .users_utils import (
    verify_user,
    get_user_from_jwt,
    get_user,
    create_jwt_token,
    store_token_in_db,
    delete_token_from_db,
    decode_jwt
)

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 31 * 24 * 60 

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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_expire = datetime.now(timezone.utc) + access_token_expires
    refresh_expire = datetime.now(timezone.utc) + refresh_token_expires
    access_token = create_jwt_token({"sub": user.username, "jti": str(jti), "exp": access_expire})
    refresh_token = create_jwt_token({"sub": user.username, "jti": str(jti), "exp": refresh_expire})
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

#TODO: refresh endpoint

#TODO: registration endpoint

#TODO: logout from all devices