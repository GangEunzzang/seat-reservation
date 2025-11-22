from abc import ABC, abstractmethod

from app.user.domain.user import User
from app.user.domain.user_register_request import UserRegisterRequest


class UserCommandUseCase(ABC):

	@abstractmethod
	async def register(self, request: UserRegisterRequest) -> User:
		"""사용자 등록"""
		pass

	@abstractmethod
	async def register_bulk(self, requests: list[UserRegisterRequest]) -> list[User]:
		"""사용자 다건 등록"""
		pass

	@abstractmethod
	async def delete(self, user_id: int) -> None:
		"""사용자 삭제"""
		pass
