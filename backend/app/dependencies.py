import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import config
from .database.client import DatabaseClient
from .models import User

database = DatabaseClient(config.DATABASE_URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "jti": str(uuid.uuid4())},
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

def get_token_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception

    if database.is_token_revoked(payload.get("jti")):
        raise credentials_exception

    return payload

async def get_current_user(payload: Annotated[dict, Depends(get_token_payload)]) -> User:
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise credentials_exception

    user = database.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
