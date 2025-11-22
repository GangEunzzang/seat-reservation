"""Reservation API Router"""
from fastapi import APIRouter, Depends, status

from api.v1.reservation.reservation_request import ReservationCreateRequest, ReservationCancelRequest
from api.v1.reservation.reservation_response import ReservationResponse
from core.response.api_response import ApiResponse
from app.dependencies import get_reservation_command_service, get_reservation_query_service
from app.reservation.application.reservation_command_service import ReservationCommandService
from app.reservation.application.reservation_query_service import ReservationQueryService

router = APIRouter(prefix="/reservation")


@router.post("", response_model=ApiResponse[ReservationResponse], status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: ReservationCreateRequest,
    service: ReservationCommandService = Depends(get_reservation_command_service)
):
    """예약 생성"""
    reservation = await service.create(request.user_id, request.seat_id, request.password)
    return ApiResponse.success(ReservationResponse.model_validate(reservation), message="예약 생성 완료")


@router.get("/{reservation_id}", response_model=ApiResponse[ReservationResponse])
async def get_reservation(
    reservation_id: int,
    service: ReservationQueryService = Depends(get_reservation_query_service)
):
    """예약 조회"""
    reservation = await service.get_reservation_by_id(reservation_id)
    return ApiResponse.success(ReservationResponse.model_validate(reservation), message="예약 조회 성공")


@router.get("", response_model=ApiResponse[list[ReservationResponse]])
async def list_reservations(
    service: ReservationQueryService = Depends(get_reservation_query_service)
):
    """예약 목록 조회"""
    reservations = await service.get_reservation_list_all()
    reservation_list = [ReservationResponse.model_validate(reservation) for reservation in reservations]
    return ApiResponse.success(reservation_list, message="예약 목록 조회 성공")


@router.patch("/{reservation_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: int,
    request: ReservationCancelRequest,
    service: ReservationCommandService = Depends(get_reservation_command_service)
):
    """예약 취소"""
    await service.cancel(reservation_id, request.password)
    return None


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    service: ReservationCommandService = Depends(get_reservation_command_service)
):
    """예약 삭제"""
    await service.delete(reservation_id)
    return None
