"""Reservation API Request DTOs"""
from pydantic import BaseModel


class ReservationCreateRequest(BaseModel):
    user_id: int
    seat_id: int
    password: str


class ReservationCancelRequest(BaseModel):
    password: str
