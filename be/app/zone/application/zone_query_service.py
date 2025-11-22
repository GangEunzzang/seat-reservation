from core.exception.domain_exception import DomainException, ErrorCode
from app.zone.application.ports.inbound.zone_query_use_case import ZoneQueryUseCase
from app.zone.application.ports.outbound.zone_repository import ZoneRepository
from app.zone.domain.zone import Zone


class ZoneQueryService(ZoneQueryUseCase):

	def __init__(self, zone_repository: ZoneRepository):
		self.zone_repository = zone_repository

	async def get_zone_by_id(self, zone_id: int) -> Zone:
		zone = await self.zone_repository.find_by_id(zone_id)
		if not zone:
			raise DomainException(ErrorCode.ZONE_NOT_FOUND)
		return zone

	async def get_zones_by_episode_id(self, episode_id: int) -> list[Zone]:
		return await self.zone_repository.find_all_by_episode_id(episode_id)
