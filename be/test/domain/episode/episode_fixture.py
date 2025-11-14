"""Episode 도메인 테스트 Fixture"""

from datetime import date

from app.domain.episode.domain.episode import Episode


class EpisodeFixture:
	"""Episode 도메인 테스트 데이터 생성 헬퍼"""

	@staticmethod
	def create_episode(
		year: int = 2024,
		name: str = "2024 연간 총회",
		start_date: date = date(2024, 1, 1),
		end_date: date = date(2024, 12, 31)
	) -> Episode:
		"""Episode 엔티티 생성"""
		return Episode.create(
			year=year,
			name=name,
			start_date=start_date,
			end_date=end_date
		)

	@staticmethod
	def create_multiple_episodes(years: list[int] = None) -> list[Episode]:
		"""여러 개의 Episode 엔티티 생성"""
		if years is None:
			years = [2022, 2023, 2024]

		episodes = []
		for year in years:
			episode = EpisodeFixture.create_episode(
				year=year,
				name=f"{year} 연간 총회",
				start_date=date(year, 1, 1),
				end_date=date(year, 12, 31)
			)
			episodes.append(episode)
		return episodes
