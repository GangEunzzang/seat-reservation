"""Table API Request DTOs"""
from pydantic import BaseModel


class TableCreateRequest(BaseModel):
    episode_id: int
    zone_id: int
    x: int
    y: int
    name: str


class TableUpdatePositionRequest(BaseModel):
    x: int
    y: int
