from core.exception.domain_exception import DomainException, ErrorCode
from app.zone.application.ports.inbound.zone_command_use_case import ZoneCommandUseCase
from app.zone.application.ports.outbound.zone_repository import ZoneRepository
from app.zone.domain.zone import Zone


class ZoneCommandService(ZoneCommandUseCase):

	def __init__(self, zone_repository: ZoneRepository):
		self.zone_repository = zone_repository

	async def create(self, episode_id: int, code: str, name: str) -> Zone:
		zone = Zone.create(episode_id=episode_id, code=code, name=name)
		return await self.zone_repository.save(zone)

	async def update_name(self, zone_id: int, name: str) -> Zone:
		zone = await self.zone_repository.find_by_id(zone_id)
		if not zone:
			raise DomainException(ErrorCode.ZONE_NOT_FOUND)

		zone.update_name(name)
		return await self.zone_repository.save(zone)

	async def delete(self, zone_id: int) -> None:
		zone = await self.zone_repository.find_by_id(zone_id)
		if not zone:
			raise DomainException(ErrorCode.ZONE_NOT_FOUND)

		await self.zone_repository.delete(zone_id)
