"""Episode API Router"""
from fastapi import APIRouter, Depends, status

from api.v1.episode.episode_request import EpisodeCreateRequest
from api.v1.episode.episode_response import EpisodeResponse
from core.response.api_response import ApiResponse
from app.dependencies import get_episode_command_service, get_episode_query_service
from app.episode.application.episode_command_service import EpisodeCommandService
from app.episode.application.episode_query_service import EpisodeQueryService

router = APIRouter(prefix="/episode")


@router.post("", response_model=ApiResponse[EpisodeResponse], status_code=status.HTTP_201_CREATED)
async def create_episode(
    request: EpisodeCreateRequest,
    service: EpisodeCommandService = Depends(get_episode_command_service)
):
    """에피소드 생성"""
    episode = await service.create(request.year, request.name, request.start_date, request.end_date)
    return ApiResponse.success(EpisodeResponse.model_validate(episode), message="에피소드 생성 완료")


@router.get("/{episode_id}", response_model=ApiResponse[EpisodeResponse])
async def get_episode(
    episode_id: int,
    service: EpisodeQueryService = Depends(get_episode_query_service)
):
    """에피소드 조회"""
    episode = await service.get_episode_by_id(episode_id)
    return ApiResponse.success(EpisodeResponse.model_validate(episode), message="에피소드 조회 성공")


@router.get("", response_model=ApiResponse[list[EpisodeResponse]])
async def list_episodes(
    service: EpisodeQueryService = Depends(get_episode_query_service)
):
    """에피소드 목록 조회"""
    episodes = await service.get_episode_list_all()
    episode_list = [EpisodeResponse.model_validate(episode) for episode in episodes]
    return ApiResponse.success(episode_list, message="에피소드 목록 조회 성공")


@router.delete("/{episode_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_episode(
    episode_id: int,
    service: EpisodeCommandService = Depends(get_episode_command_service)
):
    """에피소드 삭제"""
    await service.delete(episode_id)
    return None
