from abc import ABC, abstractmethod

from app.user.domain.user import User


class UserQueryUseCase(ABC):

	@abstractmethod
	async def get_user_by_id(self, user_id: int) -> User:
		"""ID로 사용자 조회"""
		pass

	@abstractmethod
	async def get_user_list_all(self) -> list[User]:
		"""전체 사용자 목록 조회"""
		pass
