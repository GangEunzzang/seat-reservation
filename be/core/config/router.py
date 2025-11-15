from fastapi import FastAPI

from api.v1.user.user_router import router as user_router
from api.v1.table.table_router import router as table_router


def register_routers(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/api/v1", tags=["Users"])
    app.include_router(table_router, prefix="/api/v1", tags=["Tables"])
