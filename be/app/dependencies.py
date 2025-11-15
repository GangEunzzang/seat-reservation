from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_async_session
from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_command_service import UserCommandService
from app.user.application.user_query_service import UserQueryService
from app.table.adapter.outbound.persistence.sqlalchemy_table_repository import SQLAlchemyTableRepository
from app.table.application.table_command_service import TableCommandService
from app.table.application.table_query_service import TableQueryService
from app.seat.adapter.outbound.persistence.sqlalchemy_seat_repository import SQLAlchemySeatRepository
from app.seat.application.seat_command_service import SeatCommandService
from app.seat.application.seat_query_service import SeatQueryService
from app.episode.adapter.outbound.persistence.sqlalchemy_episode_repository import SQLAlchemyEpisodeRepository
from app.episode.application.episode_command_service import EpisodeCommandService
from app.episode.application.episode_query_service import EpisodeQueryService


# User Services
def get_user_command_service(session: AsyncSession = Depends(get_async_session)) -> UserCommandService:
    repository = SQLAlchemyUserRepository(session)
    return UserCommandService(repository)


def get_user_query_service(session: AsyncSession = Depends(get_async_session)) -> UserQueryService:
    repository = SQLAlchemyUserRepository(session)
    return UserQueryService(repository)


# Table Services
def get_table_command_service(session: AsyncSession = Depends(get_async_session)) -> TableCommandService:
    repository = SQLAlchemyTableRepository(session)
    return TableCommandService(repository)


def get_table_query_service(session: AsyncSession = Depends(get_async_session)) -> TableQueryService:
    repository = SQLAlchemyTableRepository(session)
    return TableQueryService(repository)


# Seat Services
def get_seat_command_service(session: AsyncSession = Depends(get_async_session)) -> SeatCommandService:
    repository = SQLAlchemySeatRepository(session)
    return SeatCommandService(repository)


def get_seat_query_service(session: AsyncSession = Depends(get_async_session)) -> SeatQueryService:
    repository = SQLAlchemySeatRepository(session)
    return SeatQueryService(repository)


# Episode Services
def get_episode_command_service(session: AsyncSession = Depends(get_async_session)) -> EpisodeCommandService:
    repository = SQLAlchemyEpisodeRepository(session)
    return EpisodeCommandService(repository)


def get_episode_query_service(session: AsyncSession = Depends(get_async_session)) -> EpisodeQueryService:
    repository = SQLAlchemyEpisodeRepository(session)
    return EpisodeQueryService(repository)


