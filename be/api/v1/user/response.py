"""User API Response DTOs"""
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    user_code: str
    name: str
    department: str | None = None
    position: str | None = None
    phone_number: str | None = None
    episode_id: int

    model_config = ConfigDict(from_attributes=True)
