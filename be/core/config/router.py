from fastapi import FastAPI

from api.v1.user.user_router import router as user_router
from api.v1.table.table_router import router as table_router
from api.v1.seat.seat_router import router as seat_router
from api.v1.episode.episode_router import router as episode_router
from api.v1.reservation.reservation_router import router as reservation_router


def register_routers(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/api/v1", tags=["Users"])
    app.include_router(table_router, prefix="/api/v1", tags=["Tables"])
    app.include_router(seat_router, prefix="/api/v1", tags=["Seats"])
    app.include_router(episode_router, prefix="/api/v1", tags=["Episodes"])
    app.include_router(reservation_router, prefix="/api/v1", tags=["Reservations"])
