"""라우터 등록"""
from fastapi import FastAPI

from app.adapter.inbound.api.v1.router import api_router


def register_routers(app: FastAPI) -> None:
	# API v1
	app.include_router(api_router, prefix="/api/v1")

