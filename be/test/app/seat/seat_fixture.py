"""Seat 도메인 테스트 Fixture"""
from httpx import AsyncClient

from app.seat.domain.seat import Seat


class SeatFixture:
	"""Seat 도메인 테스트 데이터 생성 헬퍼"""

	@staticmethod
	def create_seat(table_id: int = 1, seat_number: int = 1) -> Seat:
		"""Seat 엔티티 생성"""
		return Seat.create(table_id=table_id, seat_number=seat_number)

	@staticmethod
	def create_multiple_seats(table_id: int = 1, count: int = 10) -> list[Seat]:
		"""여러 개의 Seat 엔티티 생성"""
		seats = []
		for i in range(1, count + 1):
			seat = SeatFixture.create_seat(table_id=table_id, seat_number=i)
			seats.append(seat)
		return seats

	@staticmethod
	def create_request_dict(table_id: int = 1, seat_number: int = 1) -> dict:
		"""API 요청 body dict 생성"""
		return {"table_id": table_id, "seat_number": seat_number}

	@staticmethod
	async def create_via_api(client: AsyncClient, table_id: int = 1, seat_number: int = 1) -> dict:
		"""API를 통해 좌석 생성 후 응답 데이터 반환"""
		request_data = SeatFixture.create_request_dict(table_id, seat_number)
		response = await client.post("/api/v1/seat", json=request_data)
		return response.json()["data"]

	@staticmethod
	async def create_multiple_via_api(client: AsyncClient, table_id: int = 1, count: int = 10) -> list[dict]:
		"""API를 통해 여러 좌석 생성"""
		seats = []
		for i in range(1, count + 1):
			seat = await SeatFixture.create_via_api(client, table_id, i)
			seats.append(seat)
		return seats
