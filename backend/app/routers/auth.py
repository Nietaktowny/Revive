from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import create_access_token, database, get_token_payload

router = APIRouter(tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user = database.validate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}

@router.post("/logout")
def logout(payload: Annotated[dict, Depends(get_token_payload)]) -> dict[str, str]:
    jti = payload.get("jti")
    if jti is not None:
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        database.revoke_token(jti, expires_at)
    return {"status": "ok"}
