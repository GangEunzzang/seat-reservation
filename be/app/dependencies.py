from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_async_session
from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_command_service import UserCommandService
from app.user.application.user_query_service import UserQueryService


# User Services
def get_user_command_service(session: AsyncSession = Depends(get_async_session)) -> UserCommandService:
    repository = SQLAlchemyUserRepository(session)
    return UserCommandService(repository)


def get_user_query_service(session: AsyncSession = Depends(get_async_session)) -> UserQueryService:
    repository = SQLAlchemyUserRepository(session)
    return UserQueryService(repository)


