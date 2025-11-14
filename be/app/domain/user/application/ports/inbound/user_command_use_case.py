from abc import ABC, abstractmethod

from app.domain.user.application.dto.user_command import RegisterUserCommand
from app.domain.user.domain.user import User


class UserCommandUseCase(ABC):

	@abstractmethod
	async def register(self, command: RegisterUserCommand) -> User:
		"""사용자 등록"""
		pass

	@abstractmethod
	async def delete(self, user_id: int) -> None:
		"""사용자 삭제"""
		pass
