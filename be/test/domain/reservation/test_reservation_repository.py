import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.reservation.adapter.outbound.persistence.sqlalchemy_reservation_repository import SQLAlchemyReservationRepository
from test.domain.reservation.reservation_fixture import ReservationFixture


@pytest.fixture
def reservation_repository(async_session: AsyncSession) -> SQLAlchemyReservationRepository:
	return SQLAlchemyReservationRepository(async_session)


@pytest.mark.asyncio
async def test_save_reservation(reservation_repository):
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=10)
	saved_reservation = await reservation_repository.save(reservation)
	assert saved_reservation.id is not None
	assert saved_reservation.user_id == 1
	assert saved_reservation.seat_id == 10


@pytest.mark.asyncio
async def test_find_by_id(reservation_repository):
	reservation = ReservationFixture.create_reservation(user_id=2, seat_id=20)
	saved_reservation = await reservation_repository.save(reservation)
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)
	assert found_reservation is not None
	assert found_reservation.id == saved_reservation.id
	assert found_reservation.user_id == 2
	assert found_reservation.seat_id == 20


@pytest.mark.asyncio
async def test_find_by_id_not_found(reservation_repository):
	found_reservation = await reservation_repository.find_by_id(9999)
	assert found_reservation is None


@pytest.mark.asyncio
async def test_find_all(reservation_repository):
	reservations = ReservationFixture.create_multiple_reservations([1, 2, 3], [10, 20, 30])
	for reservation in reservations:
		await reservation_repository.save(reservation)
	all_reservations = await reservation_repository.find_all()
	assert len(all_reservations) == 3


@pytest.mark.asyncio
async def test_delete(reservation_repository):
	reservation = ReservationFixture.create_reservation(user_id=3, seat_id=30)
	saved_reservation = await reservation_repository.save(reservation)
	await reservation_repository.delete(saved_reservation.id)
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)
	assert found_reservation is None
