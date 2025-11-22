from datetime import date

from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from app.episode.application.ports.inbound.episode_command_use_case import EpisodeCommandUseCase
from app.episode.application.ports.outbound.episode_repository import EpisodeRepository
from app.episode.domain.episode import Episode
from app.zone.application.ports.outbound.zone_repository import ZoneRepository
from app.zone.domain.zone import Zone


class EpisodeCommandService(EpisodeCommandUseCase):

	def __init__(self, episode_repository: EpisodeRepository, zone_repository: ZoneRepository):
		self.episode_repository = episode_repository
		self.zone_repository = zone_repository

	async def create(self, year: int, name: str, start_date: date, end_date: date) -> Episode:
		# Episode 생성
		episode = Episode.create(year=year, name=name, start_date=start_date, end_date=end_date)
		saved_episode = await self.episode_repository.save(episode)

		# 기본 Zone 4개 자동 생성 (A, B, C, D)
		default_zones = [
			("A", "A구역"),
			("B", "B구역"),
			("C", "C구역"),
			("D", "D구역"),
		]
		for code, zone_name in default_zones:
			zone = Zone.create(episode_id=saved_episode.id, code=code, name=zone_name)
			await self.zone_repository.save(zone)

		return saved_episode

	async def delete(self, episode_id: int) -> None:
		episode = await self.episode_repository.find_by_id(episode_id)
		if not episode:
			raise DomainException(ErrorCode.EPISODE_NOT_FOUND)

		await self.episode_repository.delete(episode_id)
