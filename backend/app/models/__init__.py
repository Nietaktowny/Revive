from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
import bcrypt

class User(BaseModel):
    id: int | None
    email: str
    created_at: datetime
    updated_at: datetime
    password_hash: str
    is_active: bool
    username: str
    first_name: str | None = None
    last_name: str | None = None

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    username: str
    first_name: str | None = None
    last_name: str | None = None