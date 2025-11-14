import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.reservation.adapter.outbound.persistence.sqlalchemy_reservation_repository import SQLAlchemyReservationRepository
from test.domain.reservation.reservation_fixture import ReservationFixture


@pytest.fixture
def reservation_repository(async_session: AsyncSession) -> SQLAlchemyReservationRepository:
	return SQLAlchemyReservationRepository(async_session)


@pytest.mark.asyncio
async def test_save_reservation(reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=10)

	# When
	saved_reservation = await reservation_repository.save(reservation)

	# Then
	assert saved_reservation.id is not None
	assert saved_reservation.user_id == 1
	assert saved_reservation.seat_id == 10


@pytest.mark.asyncio
async def test_find_by_id(reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=2, seat_id=20)
	saved_reservation = await reservation_repository.save(reservation)

	# When
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)

	# Then
	assert found_reservation is not None
	assert found_reservation.id == saved_reservation.id
	assert found_reservation.user_id == 2
	assert found_reservation.seat_id == 20


@pytest.mark.asyncio
async def test_find_by_id_not_found(reservation_repository):
	# Given
	NON_EXISTENT_RESERVATION_ID = 9999

	# When
	found_reservation = await reservation_repository.find_by_id(NON_EXISTENT_RESERVATION_ID)

	# Then
	assert found_reservation is None


@pytest.mark.asyncio
async def test_find_all(reservation_repository):
	# Given
	reservations = ReservationFixture.create_multiple_reservations([1, 2, 3], [10, 20, 30])
	for reservation in reservations:
		await reservation_repository.save(reservation)

	# When
	all_reservations = await reservation_repository.find_all()

	# Then
	assert len(all_reservations) == 3


@pytest.mark.asyncio
async def test_delete(reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=3, seat_id=30)
	saved_reservation = await reservation_repository.save(reservation)

	# When
	await reservation_repository.delete(saved_reservation.id)

	# Then
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)
	assert found_reservation is None
