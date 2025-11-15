"""Seat API Request DTOs"""
from pydantic import BaseModel


class SeatCreateRequest(BaseModel):
    table_id: int
    seat_number: int
