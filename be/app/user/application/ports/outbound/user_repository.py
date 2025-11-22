from abc import ABC, abstractmethod
from typing import Optional

from app.user.domain.user import User


class UserRepository(ABC):
	@abstractmethod
	async def save(self, user: User) -> User:
		pass

	@abstractmethod
	async def save_all(self, users: list[User]) -> list[User]:
		pass

	@abstractmethod
	async def find_by_id(self, user_id: int) -> Optional[User]:
		pass

	@abstractmethod
	async def find_all(self) -> list[User]:
		pass

	@abstractmethod
	async def delete(self, user_id: int) -> None:
		pass
