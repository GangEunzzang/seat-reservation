"""Seat API Router"""
from fastapi import APIRouter, Depends, status

from api.v1.seat.seat_request import SeatCreateRequest
from api.v1.seat.seat_response import SeatResponse
from core.response.api_response import ApiResponse
from app.dependencies import get_seat_command_service, get_seat_query_service
from app.seat.application.seat_command_service import SeatCommandService
from app.seat.application.seat_query_service import SeatQueryService

router = APIRouter(prefix="/seat")


@router.post("", response_model=ApiResponse[SeatResponse], status_code=status.HTTP_201_CREATED)
async def create_seat(
    request: SeatCreateRequest,
    service: SeatCommandService = Depends(get_seat_command_service)
):
    """좌석 생성"""
    seat = await service.create(request.table_id, request.seat_number)
    return ApiResponse.success(SeatResponse.model_validate(seat), message="좌석 생성 완료")


@router.get("/{seat_id}", response_model=ApiResponse[SeatResponse])
async def get_seat(
    seat_id: int,
    service: SeatQueryService = Depends(get_seat_query_service)
):
    """좌석 조회"""
    seat = await service.get_seat_by_id(seat_id)
    return ApiResponse.success(SeatResponse.model_validate(seat), message="좌석 조회 성공")


@router.get("", response_model=ApiResponse[list[SeatResponse]])
async def list_seats(
    service: SeatQueryService = Depends(get_seat_query_service)
):
    """좌석 목록 조회"""
    seats = await service.get_seat_list_all()
    seat_list = [SeatResponse.model_validate(seat) for seat in seats]
    return ApiResponse.success(seat_list, message="좌석 목록 조회 성공")


@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seat(
    seat_id: int,
    service: SeatCommandService = Depends(get_seat_command_service)
):
    """좌석 삭제"""
    await service.delete(seat_id)
    return None
