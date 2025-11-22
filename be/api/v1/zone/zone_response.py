"""Zone API Response DTOs"""
from pydantic import BaseModel, ConfigDict


class ZoneResponse(BaseModel):
    id: int
    episode_id: int
    code: str
    name: str

    model_config = ConfigDict(from_attributes=True)
