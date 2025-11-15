"""Episode API Request DTOs"""
from datetime import date
from pydantic import BaseModel


class EpisodeCreateRequest(BaseModel):
    year: int
    name: str
    start_date: date
    end_date: date
