"""Reservation 도메인 테스트 Fixture"""

from app.domain.reservation.domain.reservation import Reservation


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
