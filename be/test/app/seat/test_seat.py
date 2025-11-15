from test.app.seat.seat_fixture import SeatFixture


def test_create_seat():
	"""Seat 생성 테스트"""
	# Given & When
	seat = SeatFixture.create_seat(table_id=1, seat_number=5)

	# Then
	assert seat.table_id == 1
	assert seat.seat_number == 5
