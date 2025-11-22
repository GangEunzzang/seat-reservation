"""FastAPI 애플리케이션 팩토리"""
from fastapi import FastAPI

from core.config.cors_config import register_cors
from core.config.event import register_events
from core.config.router import register_routers
from core.middleware.exception_middleware import exceptions_handler


def create_app() -> FastAPI:
	app = FastAPI(
		title="Seat Reservation API",
		description="좌석 예약 시스템 API",
		version="1.0.0",
		docs_url="/docs",
		redoc_url="/redoc",
	)

	register_cors(app)
	exceptions_handler(app)
	register_events(app)
	register_routers(app)

	@app.get("/", tags=["Root"])
	async def root():
		return {
			"message": "Seat Reservation API",
			"version": "1.0.0",
			"docs": "/docs"
		}

	@app.get("/health", tags=["Health"])
	async def health_check():
		return {"status": "healthy"}

	return app
