"""Reservation 도메인 테스트 Fixture"""
from httpx import AsyncClient

from app.reservation.domain.reservation import Reservation


class ReservationFixture:
	"""Reservation 도메인 테스트 데이터 생성 헬퍼"""

	@staticmethod
	def create_reservation(user_id: int = 1, seat_id: int = 1) -> Reservation:
		"""Reservation 엔티티 생성"""
		return Reservation.create(user_id=user_id, seat_id=seat_id)

	@staticmethod
	def create_cancelled_reservation(user_id: int = 1, seat_id: int = 1) -> Reservation:
		"""취소된 Reservation 엔티티 생성"""
		reservation = ReservationFixture.create_reservation(user_id=user_id, seat_id=seat_id)
		reservation.cancel()
		return reservation

	@staticmethod
	def create_multiple_reservations(user_ids: list[int], seat_ids: list[int]) -> list[Reservation]:
		"""여러 개의 Reservation 엔티티 생성"""
		if len(user_ids) != len(seat_ids):
			raise ValueError("user_ids and seat_ids must have the same length")

		reservations = []
		for user_id, seat_id in zip(user_ids, seat_ids):
			reservation = ReservationFixture.create_reservation(user_id=user_id, seat_id=seat_id)
			reservations.append(reservation)
		return reservations

	@staticmethod
	def create_request_dict(user_id: int = 1, seat_id: int = 1) -> dict:
		"""API 요청 body dict 생성"""
		return {"user_id": user_id, "seat_id": seat_id}

	@staticmethod
	async def create_via_api(client: AsyncClient, user_id: int = 1, seat_id: int = 1) -> dict:
		"""API를 통해 예약 생성 후 응답 데이터 반환"""
		request_data = ReservationFixture.create_request_dict(user_id, seat_id)
		response = await client.post("/api/v1/reservation", json=request_data)
		return response.json()["data"]

	@staticmethod
	async def create_multiple_via_api(client: AsyncClient, user_ids: list[int], seat_ids: list[int]) -> list[dict]:
		"""API를 통해 여러 예약 생성"""
		if len(user_ids) != len(seat_ids):
			raise ValueError("user_ids and seat_ids must have the same length")

		reservations = []
		for user_id, seat_id in zip(user_ids, seat_ids):
			reservation = await ReservationFixture.create_via_api(client, user_id, seat_id)
			reservations.append(reservation)
		return reservations
