"""애플리케이션 이벤트 핸들러"""
from fastapi import FastAPI

from core.config.database import init_db, async_engine


async def on_startup():
	"""애플리케이션 시작 시 실행"""
	await init_db()
	print("✅ Database initialized")


async def on_shutdown():
	"""애플리케이션 종료 시 실행"""
	await async_engine.dispose()
	print("✅ Database connections closed")


def register_events(app: FastAPI) -> None:
	"""이벤트 핸들러 등록"""
	app.add_event_handler("startup", on_startup)
	app.add_event_handler("shutdown", on_shutdown)
