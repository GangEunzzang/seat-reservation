import pytest

from test.domain.reservation.reservation_fixture import ReservationFixture
from app.domain.reservation.domain.reservation_status import ReservationStatus


def test_create_reservation():
	"""Reservation 생성 테스트"""
	# Given & When
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=1)

	# Then
	assert reservation.user_id == 1
	assert reservation.seat_id == 1
	assert reservation.get_status() == ReservationStatus.RESERVED
	assert reservation.get_status().code == "reserve"
	assert reservation.reserved_at is not None
	assert reservation.cancelled_at is None
	assert reservation.is_active() is True
	assert reservation.is_cancelled() is False


def test_cancel_reservation():
	"""Reservation 취소 테스트"""
	# Given
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=1)

	# When
	reservation.cancel()

	# Then
	assert reservation.get_status() == ReservationStatus.CANCELLED
	assert reservation.get_status().code == "cancel"
	assert reservation.cancelled_at is not None
	assert reservation.is_active() is False
	assert reservation.is_cancelled() is True


def test_cancel_already_cancelled_reservation():
	"""이미 취소된 Reservation 재취소 시 예외 발생 테스트"""
	# Given
	reservation = ReservationFixture.create_cancelled_reservation(user_id=1, seat_id=1)

	# When & Then
	with pytest.raises(ValueError, match="Already cancelled reservation"):
		reservation.cancel()
