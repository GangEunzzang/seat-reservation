"""Table API Response DTOs"""
from pydantic import BaseModel, ConfigDict


class TableResponse(BaseModel):
    id: int
    episode_id: int

    model_config = ConfigDict(from_attributes=True)
