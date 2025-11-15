"""Seat 도메인 테스트 Fixture"""

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
