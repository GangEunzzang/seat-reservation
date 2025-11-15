from abc import ABC, abstractmethod
from typing import Optional

from app.reservation.domain.reservation import Reservation


class ReservationRepository(ABC):
    @abstractmethod
    async def save(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    async def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
        pass

    @abstractmethod
    async def find_all(self) -> list[Reservation]:
        pass

    @abstractmethod
    async def delete(self, reservation_id: int) -> None:
        pass

    @abstractmethod
    async def find_active_by_seat_id(self, seat_id: int) -> Optional[Reservation]:
        """활성 상태의 예약을 좌석 ID로 조회"""
        pass
