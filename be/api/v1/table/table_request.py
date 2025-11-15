"""Table API Request DTOs"""
from pydantic import BaseModel


class TableCreateRequest(BaseModel):
    episode_id: int
