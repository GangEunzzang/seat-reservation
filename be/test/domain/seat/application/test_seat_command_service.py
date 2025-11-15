import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DomainException, ErrorCode
from app.domain.seat.adapter.outbound.persistence.sqlalchemy_seat_repository import SQLAlchemySeatRepository
from app.domain.seat.application.seat_command_service import SeatCommandService
from test.domain.seat.seat_fixture import SeatFixture


@pytest.fixture
def seat_repository(async_session: AsyncSession) -> SQLAlchemySeatRepository:
	return SQLAlchemySeatRepository(async_session)


@pytest.fixture
def seat_command_service(seat_repository) -> SeatCommandService:
	return SeatCommandService(seat_repository)


@pytest.mark.asyncio
async def test_create_seat(seat_command_service):
	# Given
	table_id = 1
	seat_number = 1

	# When
	result = await seat_command_service.create(table_id, seat_number)

	# Then
	assert result.id is not None
	assert result.table_id == table_id
	assert result.seat_number == seat_number


@pytest.mark.asyncio
async def test_delete_seat(seat_command_service, seat_repository):
	# Given
	seat = SeatFixture.create_seat(table_id=1, seat_number=1)
	saved_seat = await seat_repository.save(seat)

	# When
	await seat_command_service.delete(saved_seat.id)

	# Then
	found_seat = await seat_repository.find_by_id(saved_seat.id)
	assert found_seat is None


@pytest.mark.asyncio
async def test_delete_seat_not_found(seat_command_service):
	# Given
	NON_EXISTENT_SEAT_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await seat_command_service.delete(NON_EXISTENT_SEAT_ID)

	assert exc_info.value.error_code == ErrorCode.SEAT_NOT_FOUND
