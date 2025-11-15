"""Seat API Response DTOs"""
from pydantic import BaseModel, ConfigDict


class SeatResponse(BaseModel):
    id: int
    table_id: int
    seat_number: int

    model_config = ConfigDict(from_attributes=True)
