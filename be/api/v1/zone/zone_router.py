"""Zone API Router"""
from fastapi import APIRouter, Depends, status

from api.v1.zone.zone_request import ZoneCreateRequest, ZoneUpdateRequest
from api.v1.zone.zone_response import ZoneResponse
from core.response.api_response import ApiResponse
from app.dependencies import get_zone_command_service, get_zone_query_service
from app.zone.application.zone_command_service import ZoneCommandService
from app.zone.application.zone_query_service import ZoneQueryService

router = APIRouter(prefix="/zone")


@router.post("", response_model=ApiResponse[ZoneResponse], status_code=status.HTTP_201_CREATED)
async def create_zone(
    request: ZoneCreateRequest,
    service: ZoneCommandService = Depends(get_zone_command_service)
):
    """Zone 생성"""
    zone = await service.create(request.episode_id, request.code, request.name)
    return ApiResponse.success(ZoneResponse.model_validate(zone), message="Zone 생성 완료")


@router.get("/{zone_id}", response_model=ApiResponse[ZoneResponse])
async def get_zone(
    zone_id: int,
    service: ZoneQueryService = Depends(get_zone_query_service)
):
    """Zone 조회"""
    zone = await service.get_zone_by_id(zone_id)
    return ApiResponse.success(ZoneResponse.model_validate(zone), message="Zone 조회 성공")


@router.get("/episode/{episode_id}", response_model=ApiResponse[list[ZoneResponse]])
async def list_zones_by_episode(
    episode_id: int,
    service: ZoneQueryService = Depends(get_zone_query_service)
):
    """Episode별 Zone 목록 조회"""
    zones = await service.get_zones_by_episode_id(episode_id)
    zone_list = [ZoneResponse.model_validate(zone) for zone in zones]
    return ApiResponse.success(zone_list, message="Zone 목록 조회 성공")


@router.patch("/{zone_id}", response_model=ApiResponse[ZoneResponse])
async def update_zone_name(
    zone_id: int,
    request: ZoneUpdateRequest,
    service: ZoneCommandService = Depends(get_zone_command_service)
):
    """Zone 이름 수정"""
    zone = await service.update_name(zone_id, request.name)
    return ApiResponse.success(ZoneResponse.model_validate(zone), message="Zone 이름 수정 완료")


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(
    zone_id: int,
    service: ZoneCommandService = Depends(get_zone_command_service)
):
    """Zone 삭제"""
    await service.delete(zone_id)
    return None
