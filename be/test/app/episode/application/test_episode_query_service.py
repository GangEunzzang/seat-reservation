import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.episode.adapter.outbound.persistence.sqlalchemy_episode_repository import SQLAlchemyEpisodeRepository
from app.episode.application.episode_query_service import EpisodeQueryService
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from test.app.episode.episode_fixture import EpisodeFixture


@pytest.fixture
def episode_repository(async_session: AsyncSession) -> SQLAlchemyEpisodeRepository:
	return SQLAlchemyEpisodeRepository(async_session)


@pytest.fixture
def episode_query_service(episode_repository) -> EpisodeQueryService:
	return EpisodeQueryService(episode_repository)


@pytest.mark.asyncio
async def test_get_episode_by_id(episode_query_service, episode_repository):
	# Given
	episode = EpisodeFixture.create_episode(year=2024, name="2024 연간 총회")
	saved_episode = await episode_repository.save(episode)

	# When
	result = await episode_query_service.get_episode_by_id(saved_episode.id)

	# Then
	assert result is not None
	assert result.id == saved_episode.id
	assert result.year == 2024
	assert result.name == "2024 연간 총회"


@pytest.mark.asyncio
async def test_get_episode_by_id_not_found(episode_query_service):
	# Given
	NON_EXISTENT_EPISODE_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await episode_query_service.get_episode_by_id(NON_EXISTENT_EPISODE_ID)

	assert exc_info.value.error_code == ErrorCode.EPISODE_NOT_FOUND


@pytest.mark.asyncio
async def test_get_episode_list_all(episode_query_service, episode_repository):
	# Given
	episodes = EpisodeFixture.create_multiple_episodes([2022, 2023, 2024])
	for episode in episodes:
		await episode_repository.save(episode)

	# When
	result = await episode_query_service.get_episode_list_all()

	# Then
	assert len(result) == 3


@pytest.mark.asyncio
async def test_get_episode_list_all_empty(episode_query_service):
	# When
	result = await episode_query_service.get_episode_list_all()

	# Then
	assert result == []
