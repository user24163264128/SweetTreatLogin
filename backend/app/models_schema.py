from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class BaseUser(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "arbitrary_types_allowed": True
    }


class UserSchema(BaseUser):
    role: str = "user"


class AdminSchema(BaseUser):
    role: str = "admin"
    permissions: list[str] = ["manage_users", "view_reports", "system_settings"]
