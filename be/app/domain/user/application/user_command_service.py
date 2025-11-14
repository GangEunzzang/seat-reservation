from app.core.exceptions import DomainException, ErrorCode
from app.domain.user.application.ports.inbound.user_command_use_case import UserCommandUseCase
from app.domain.user.application.ports.outbound.user_repository import UserRepository
from app.domain.user.domain.user import User
from app.domain.user.domain.user_register_request import UserRegisterRequest


class UserCommandService(UserCommandUseCase):

	def __init__(self, user_repository: UserRepository):
		self.user_repository = user_repository

	async def register(self, request: UserRegisterRequest) -> User:
		if await self.user_repository.exists_by_user_code(request.user_code):
			raise DomainException(ErrorCode.USER_CODE_ALREADY_EXISTS, user_code=request.user_code)

		user = User.create(request)
		return await self.user_repository.save(user)

	async def delete(self, user_id: int) -> None:
		user = await self.user_repository.find_by_id(user_id)
		if not user:
			raise DomainException(ErrorCode.USER_NOT_FOUND)

		await self.user_repository.delete(user_id)
