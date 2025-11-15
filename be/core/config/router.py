from fastapi import FastAPI

from api.v1.user.user_router import router as user_router


def register_routers(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/api/v1", tags=["Users"])
