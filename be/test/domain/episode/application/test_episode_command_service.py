import pytest
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.domain_exception import DomainException
from app.core.exception.error_code import ErrorCode
from app.domain.episode.adapter.outbound.persistence.sqlalchemy_episode_repository import SQLAlchemyEpisodeRepository
from app.domain.episode.application.episode_command_service import EpisodeCommandService
from test.domain.episode.episode_fixture import EpisodeFixture


@pytest.fixture
def episode_repository(async_session: AsyncSession) -> SQLAlchemyEpisodeRepository:
	return SQLAlchemyEpisodeRepository(async_session)


@pytest.fixture
def episode_command_service(episode_repository) -> EpisodeCommandService:
	return EpisodeCommandService(episode_repository)


@pytest.mark.asyncio
async def test_create_episode(episode_command_service):
	# Given
	year = 2024
	name = "2024 연간 총회"
	start_date = date(2024, 1, 1)
	end_date = date(2024, 12, 31)

	# When
	result = await episode_command_service.create(year, name, start_date, end_date)

	# Then
	assert result.id is not None
	assert result.year == year
	assert result.name == name
	assert result.start_date == start_date
	assert result.end_date == end_date


@pytest.mark.asyncio
async def test_delete_episode(episode_command_service, episode_repository):
	# Given
	episode = EpisodeFixture.create_episode(year=2024, name="2024 연간 총회")
	saved_episode = await episode_repository.save(episode)

	# When
	await episode_command_service.delete(saved_episode.id)

	# Then
	found_episode = await episode_repository.find_by_id(saved_episode.id)
	assert found_episode is None


@pytest.mark.asyncio
async def test_delete_episode_not_found(episode_command_service):
	# Given
	NON_EXISTENT_EPISODE_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await episode_command_service.delete(NON_EXISTENT_EPISODE_ID)

	assert exc_info.value.error_code == ErrorCode.EPISODE_NOT_FOUND
