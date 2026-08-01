from fastapi import HTTPException, status
import jwt

def decode_jwt(token: str, SECRET_KEY: str, ALGORITHM: str):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise credentials_exeption
    except jwt.ExpiredSignatureError:
        raise credentials_exeption
    return payload