"""Episode 도메인 테스트 Fixture"""
from datetime import date

from httpx import AsyncClient

from app.episode.domain.episode import Episode


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

	@staticmethod
	def create_request_dict(
		year: int = 2024,
		name: str = "2024 연간 총회",
		start_date: str = "2024-01-01",
		end_date: str = "2024-12-31"
	) -> dict:
		"""API 요청 body dict 생성"""
		return {"year": year, "name": name, "start_date": start_date, "end_date": end_date}

	@staticmethod
	async def create_via_api(client: AsyncClient, **kwargs) -> dict:
		"""API를 통해 에피소드 생성 후 응답 데이터 반환"""
		request_data = EpisodeFixture.create_request_dict(**kwargs)
		response = await client.post("/api/v1/episode", json=request_data)
		return response.json()["data"]

	@staticmethod
	async def create_multiple_via_api(client: AsyncClient, years: list[int] = None) -> list[dict]:
		"""API를 통해 여러 에피소드 생성"""
		if years is None:
			years = [2022, 2023, 2024]

		episodes = []
		for year in years:
			episode = await EpisodeFixture.create_via_api(
				client, year=year, name=f"{year} 연간 총회", start_date=f"{year}-01-01", end_date=f"{year}-12-31"
			)
			episodes.append(episode)
		return episodes
