"""Database configuration"""
from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
SQL_ECHO = os.getenv("SQL_ECHO", "True").lower() in ("true", "1", "yes")

async_engine = create_async_engine(
	DATABASE_URL,
	echo=SQL_ECHO,
	future=True,
)

AsyncSessionLocal = async_sessionmaker(
	bind=async_engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autoflush=False,
	autocommit=False,
)


class Base(DeclarativeBase):
	"""Base class for all domain entities"""
	pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	"""Provide async database session for FastAPI Depends"""
	async with AsyncSessionLocal() as session:
		try:
			yield session
			await session.commit()
		except Exception:
			await session.rollback()
			raise
		finally:
			await session.close()


async def init_db() -> None:
	"""Initialize database tables"""
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
	"""Drop all database tables"""
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
