from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_async_session
from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_command_service import UserCommandService
from app.user.application.user_query_service import UserQueryService
from app.table.adapter.outbound.persistence.sqlalchemy_table_repository import SQLAlchemyTableRepository
from app.table.application.table_command_service import TableCommandService
from app.table.application.table_query_service import TableQueryService


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


