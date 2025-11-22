from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from app.user.application.ports.inbound.user_command_use_case import UserCommandUseCase
from app.user.application.ports.outbound.user_repository import UserRepository
from app.user.domain.user import User
from app.user.domain.user_register_request import UserRegisterRequest


class UserCommandService(UserCommandUseCase):

	def __init__(self, user_repository: UserRepository):
		self.user_repository = user_repository

	async def register(self, request: UserRegisterRequest) -> User:
		user = User.create(request)
		return await self.user_repository.save(user)

	async def register_bulk(self, requests: list[UserRegisterRequest]) -> list[User]:
		"""
		사용자 다건 등록

		Note:
		- 트랜잭션은 HTTP 요청 단위로 보장
		- 중간에 하나라도 실패하면 전체가 rollback
		- SQLAlchemy 2.0 제약으로 개별 save 사용
		"""
		users = []
		for request in requests:
			user = User.create(request)
			saved_user = await self.user_repository.save(user)
			users.append(saved_user)
		return users

	async def delete(self, user_id: int) -> None:
		user = await self.user_repository.find_by_id(user_id)
		if not user:
			raise DomainException(ErrorCode.USER_NOT_FOUND)

		await self.user_repository.delete(user_id)
