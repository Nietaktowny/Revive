from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import database, get_current_user
from ..models import User, UserPublic

router = APIRouter(tags=["users"])

@router.post("/add_user")
def add_user(email: str, password: str, first_name: str, last_name: str) -> dict[str, str]:
    user = User(
        id=None,
        email=email,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        password_hash=password,
        is_active=True,
        username=email.split("@")[0],
        first_name=first_name,
        last_name=last_name
    )
    database.add_user(user)
    return {"status": "ok"}

@router.post("/current_user")
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]) -> UserPublic:
    return UserPublic.model_validate(current_user)
