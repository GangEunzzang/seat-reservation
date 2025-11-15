"""User API Router"""
from fastapi import APIRouter, Depends, status

from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from core.response.api_response import ApiResponse
from app.dependencies import get_user_command_service, get_user_query_service
from app.user.application.user_command_service import UserCommandService
from app.user.application.user_query_service import UserQueryService
from app.user.domain.user_register_request import UserRegisterRequest as DomainUserRegisterRequest
from api.v1.user.request import UserRegisterRequest
from api.v1.user.response import UserResponse

router = APIRouter()


@router.post("/users", response_model=ApiResponse.Success[UserResponse], status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    service: UserCommandService = Depends(get_user_command_service)
):
    """사용자 등록"""
    domain_request = DomainUserRegisterRequest(
        user_code=request.user_code,
        name=request.name,
        department=request.department,
        position=request.position,
        phone_number=request.phone_number,
        episode_id=request.episode_id
    )
    user = await service.register(domain_request)
    return ApiResponse.success(UserResponse.model_validate(user), message="사용자 등록 완료")


@router.get("/users/{user_id}", response_model=ApiResponse.Success[UserResponse])
async def get_user(
    user_id: int,
    service: UserQueryService = Depends(get_user_query_service)
):
    """사용자 조회"""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise DomainException(ErrorCode.USER_NOT_FOUND)
    return ApiResponse.success(UserResponse.model_validate(user), message="사용자 조회 성공")


@router.get("/users", response_model=ApiResponse.Success[list[UserResponse]])
async def list_users(
    service: UserQueryService = Depends(get_user_query_service)
):
    """사용자 목록 조회"""
    users = await service.get_user_list_all()
    user_list = [UserResponse.model_validate(user) for user in users]
    return ApiResponse.success(user_list, message="사용자 목록 조회 성공")


@router.delete("/users/{user_id}", response_model=ApiResponse.Success[None])
async def delete_user(
    user_id: int,
    service: UserCommandService = Depends(get_user_command_service)
):
    """사용자 삭제"""
    await service.delete(user_id)
    return ApiResponse.success(None, message="사용자 삭제 완료")
