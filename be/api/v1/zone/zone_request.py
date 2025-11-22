"""Zone API Request DTOs"""
from pydantic import BaseModel


class ZoneCreateRequest(BaseModel):
    episode_id: int
    code: str
    name: str


class ZoneUpdateRequest(BaseModel):
    name: str
