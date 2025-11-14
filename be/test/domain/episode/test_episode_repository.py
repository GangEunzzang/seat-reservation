import pytest
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.episode.adapter.outbound.persistence.sqlalchemy_episode_repository import SQLAlchemyEpisodeRepository
from test.domain.episode.episode_fixture import EpisodeFixture


@pytest.fixture
def episode_repository(async_session: AsyncSession) -> SQLAlchemyEpisodeRepository:
	return SQLAlchemyEpisodeRepository(async_session)


@pytest.mark.asyncio
async def test_save_episode(episode_repository):
	# Given
	episode = EpisodeFixture.create_episode(year=2024, name="2024 연간 총회")

	# When
	saved_episode = await episode_repository.save(episode)

	# Then
	assert saved_episode.id is not None
	assert saved_episode.year == 2024
	assert saved_episode.name == "2024 연간 총회"


@pytest.mark.asyncio
async def test_find_by_id(episode_repository):
	# Given
	episode = EpisodeFixture.create_episode(year=2025, name="2025 연간 총회")
	saved_episode = await episode_repository.save(episode)

	# When
	found_episode = await episode_repository.find_by_id(saved_episode.id)

	# Then
	assert found_episode is not None
	assert found_episode.id == saved_episode.id
	assert found_episode.year == 2025
	assert found_episode.name == "2025 연간 총회"


@pytest.mark.asyncio
async def test_find_by_id_not_found(episode_repository):
	# Given
	NON_EXISTENT_EPISODE_ID = 9999

	# When
	found_episode = await episode_repository.find_by_id(NON_EXISTENT_EPISODE_ID)

	# Then
	assert found_episode is None


@pytest.mark.asyncio
async def test_find_all(episode_repository):
	# Given
	episodes = EpisodeFixture.create_multiple_episodes([2022, 2023, 2024])
	for episode in episodes:
		await episode_repository.save(episode)

	# When
	all_episodes = await episode_repository.find_all()

	# Then
	assert len(all_episodes) == 3


@pytest.mark.asyncio
async def test_delete(episode_repository):
	# Given
	episode = EpisodeFixture.create_episode(year=2026, name="2026 연간 총회")
	saved_episode = await episode_repository.save(episode)

	# When
	await episode_repository.delete(saved_episode.id)

	# Then
	found_episode = await episode_repository.find_by_id(saved_episode.id)
	assert found_episode is None
