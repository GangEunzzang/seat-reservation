"""Reservation API Response DTOs"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    seat_id: int
    status: str
    reserved_at: datetime
    cancelled_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
