from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.application.ports.outbound.user_repository import UserRepository
from app.domain.user.domain.user import User


class SQLAlchemyUserRepository(UserRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, user: User) -> User:
		self.session.add(user)
		await self.session.flush()
		await self.session.refresh(user)
		return user

	async def find_by_id(self, user_id: int) -> Optional[User]:
		return await self.session.get(User, user_id)

	async def find_by_user_code(self, user_code: str) -> Optional[User]:
		stmt = select(User).where(User.user_code == user_code)
		result = await self.session.execute(stmt)
		return result.scalar_one_or_none()

	async def find_all(self) -> list[User]:
		stmt = select(User)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, user_id: int) -> None:
		stmt = delete(User).where(User.id == user_id)
		await self.session.execute(stmt)
		await self.session.flush()

	async def exists_by_user_code(self, user_code: str) -> bool:
		stmt = select(1).where(User.user_code == user_code).limit(1)
		result = await self.session.execute(stmt)
		return result.first() is not None
