import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.seat.adapter.outbound.persistence.sqlalchemy_seat_repository import SQLAlchemySeatRepository
from test.domain.seat.seat_fixture import SeatFixture


@pytest.fixture
def seat_repository(async_session: AsyncSession) -> SQLAlchemySeatRepository:
	return SQLAlchemySeatRepository(async_session)


@pytest.mark.asyncio
async def test_save_seat(seat_repository):
	seat = SeatFixture.create_seat(table_id=1, seat_number=10)
	saved_seat = await seat_repository.save(seat)
	assert saved_seat.id is not None
	assert saved_seat.table_id == 1
	assert saved_seat.seat_number == 10


@pytest.mark.asyncio
async def test_find_by_id(seat_repository):
	seat = SeatFixture.create_seat(table_id=2, seat_number=20)
	saved_seat = await seat_repository.save(seat)
	found_seat = await seat_repository.find_by_id(saved_seat.id)
	assert found_seat is not None
	assert found_seat.id == saved_seat.id
	assert found_seat.table_id == 2
	assert found_seat.seat_number == 20


@pytest.mark.asyncio
async def test_find_by_id_not_found(seat_repository):
	found_seat = await seat_repository.find_by_id(9999)
	assert found_seat is None


@pytest.mark.asyncio
async def test_find_all(seat_repository):
	seats = SeatFixture.create_multiple_seats(table_id=1, count=5)
	for seat in seats:
		await seat_repository.save(seat)
	all_seats = await seat_repository.find_all()
	assert len(all_seats) == 5


@pytest.mark.asyncio
async def test_delete(seat_repository):
	seat = SeatFixture.create_seat(table_id=3, seat_number=30)
	saved_seat = await seat_repository.save(seat)
	await seat_repository.delete(saved_seat.id)
	found_seat = await seat_repository.find_by_id(saved_seat.id)
	assert found_seat is None
