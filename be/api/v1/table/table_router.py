"""Table API Router"""
from fastapi import APIRouter, Depends, status

from api.v1.table.table_request import TableCreateRequest, TableUpdatePositionRequest
from api.v1.table.table_response import TableResponse
from core.response.api_response import ApiResponse
from app.dependencies import get_table_command_service, get_table_query_service
from app.table.application.table_command_service import TableCommandService
from app.table.application.table_query_service import TableQueryService

router = APIRouter(prefix="/table")


@router.post("", response_model=ApiResponse[TableResponse], status_code=status.HTTP_201_CREATED)
async def create_table(
    request: TableCreateRequest,
    service: TableCommandService = Depends(get_table_command_service)
):
    """테이블 생성"""
    table = await service.create(request.episode_id, request.zone_id, request.x, request.y, request.name)
    return ApiResponse.success(TableResponse.model_validate(table), message="테이블 생성 완료")


@router.patch("/{table_id}/position", response_model=ApiResponse[TableResponse])
async def update_table_position(
    table_id: int,
    request: TableUpdatePositionRequest,
    service: TableCommandService = Depends(get_table_command_service)
):
    """테이블 위치 수정"""
    table = await service.update_position(table_id, request.x, request.y)
    return ApiResponse.success(TableResponse.model_validate(table), message="테이블 위치 수정 완료")


@router.get("/{table_id}", response_model=ApiResponse[TableResponse])
async def get_table(
    table_id: int,
    service: TableQueryService = Depends(get_table_query_service)
):
    """테이블 조회"""
    table = await service.get_table_by_id(table_id)
    return ApiResponse.success(TableResponse.model_validate(table), message="테이블 조회 성공")


@router.get("", response_model=ApiResponse[list[TableResponse]])
async def list_tables(
    service: TableQueryService = Depends(get_table_query_service)
):
    """테이블 목록 조회"""
    tables = await service.get_table_list_all()
    table_list = [TableResponse.model_validate(table) for table in tables]
    return ApiResponse.success(table_list, message="테이블 목록 조회 성공")


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
    service: TableCommandService = Depends(get_table_command_service)
):
    """테이블 삭제"""
    await service.delete(table_id)
    return None
