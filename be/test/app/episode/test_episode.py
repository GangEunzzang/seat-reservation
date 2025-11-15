from datetime import date

from test.app.episode.episode_fixture import EpisodeFixture


def test_create_episode():
	"""Episode 생성 테스트"""
	# Given & When
	episode = EpisodeFixture.create_episode(
		year=2024,
		name="2024 테스트 총회",
		start_date=date(2024, 1, 1),
		end_date=date(2024, 12, 31)
	)

	# Then
	assert episode.year == 2024
	assert episode.name == "2024 테스트 총회"
	assert episode.start_date == date(2024, 1, 1)
	assert episode.end_date == date(2024, 12, 31)
