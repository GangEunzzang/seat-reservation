"""Episode API Response DTOs"""
from datetime import date
from pydantic import BaseModel, ConfigDict


class EpisodeResponse(BaseModel):
    id: int
    year: int
    name: str
    start_date: date
    end_date: date

    model_config = ConfigDict(from_attributes=True)
