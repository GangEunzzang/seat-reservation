from app.user.application.ports.inbound.user_query_use_case import UserQueryUseCase
from app.user.application.ports.outbound.user_repository import UserRepository
from app.user.domain.user import User
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode


class UserQueryService(UserQueryUseCase):

	def __init__(self, user_repository: UserRepository):
		self.user_repository = user_repository

	async def get_user_by_id(self, user_id: int) -> User:
		user = await self.user_repository.find_by_id(user_id)
		if not user:
			raise DomainException(ErrorCode.USER_NOT_FOUND)
		return user

	async def get_user_by_code(self, user_code: str) -> User:
		user = await self.user_repository.find_by_user_code(user_code)
		if not user:
			raise DomainException(ErrorCode.USER_NOT_FOUND)
		return user

	async def get_user_list_all(self) -> list[User]:
		return await self.user_repository.find_all()

	async def exists_by_user_code(self, user_code: str) -> bool:
		return await self.user_repository.exists_by_user_code(user_code)
