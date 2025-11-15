import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.seat.adapter.outbound.persistence.sqlalchemy_seat_repository import SQLAlchemySeatRepository
from app.seat.application.seat_query_service import SeatQueryService
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from test.app.seat.seat_fixture import SeatFixture


@pytest.fixture
def seat_repository(async_session: AsyncSession) -> SQLAlchemySeatRepository:
	return SQLAlchemySeatRepository(async_session)


@pytest.fixture
def seat_query_service(seat_repository) -> SeatQueryService:
	return SeatQueryService(seat_repository)


@pytest.mark.asyncio
async def test_get_seat_by_id(seat_query_service, seat_repository):
	# Given
	seat = SeatFixture.create_seat(table_id=1, seat_number=1)
	saved_seat = await seat_repository.save(seat)

	# When
	result = await seat_query_service.get_seat_by_id(saved_seat.id)

	# Then
	assert result is not None
	assert result.id == saved_seat.id
	assert result.table_id == 1
	assert result.seat_number == 1


@pytest.mark.asyncio
async def test_get_seat_by_id_not_found(seat_query_service):
	# Given
	NON_EXISTENT_SEAT_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await seat_query_service.get_seat_by_id(NON_EXISTENT_SEAT_ID)

	assert exc_info.value.error_code == ErrorCode.SEAT_NOT_FOUND


@pytest.mark.asyncio
async def test_get_seat_list_all(seat_query_service, seat_repository):
	# Given
	seats = SeatFixture.create_multiple_seats(table_id=1, count=5)
	for seat in seats:
		await seat_repository.save(seat)

	# When
	result = await seat_query_service.get_seat_list_all()

	# Then
	assert len(result) == 5


@pytest.mark.asyncio
async def test_get_seat_list_all_empty(seat_query_service):
	# When
	result = await seat_query_service.get_seat_list_all()

	# Then
	assert result == []
