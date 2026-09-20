from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .dependencies import get_current_user
from .models import User
from .routers import auth, users

app = FastAPI(title="Revive API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root(current_user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    return {"message": "Revive API is running"}
