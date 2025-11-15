from abc import ABC, abstractmethod

from app.user.domain.user import User


class UserQueryUseCase(ABC):

	@abstractmethod
	async def get_user_by_id(self, user_id: int) -> User:
		"""ID로 사용자 조회"""
		pass

	@abstractmethod
	async def get_user_by_code(self, user_code: str) -> User:
		"""사용자 코드로 조회"""
		pass

	@abstractmethod
	async def get_user_list_all(self) -> list[User]:
		"""전체 사용자 목록 조회"""
		pass

	@abstractmethod
	async def exists_by_user_code(self, user_code: str) -> bool:
		"""사용자 코드 존재 여부 확인"""
		pass
