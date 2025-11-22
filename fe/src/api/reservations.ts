import {apiClient} from './client';
import type {ApiResponse} from './types';

export interface ReservationCreateRequest {
    user_id: number;
    seat_id: number;
    password: string;
}

export interface ReservationCancelRequest {
    password: string;
}

export interface ReservationResponse {
    id: number;
    user_id: number;
    seat_id: number;
    status: string;
    reserved_at: string;
    cancelled_at: string | null;
}

export const reservationApi = {
    /**
     * 예약 생성
     */
    create: async (request: ReservationCreateRequest): Promise<ReservationResponse> => {
        const response = await apiClient.post<ApiResponse<ReservationResponse>>('/reservation', request);
        return response.data;
    },

    /**
     * 예약 취소
     */
    cancel: async (reservationId: number, password: string): Promise<void> => {
        const request: ReservationCancelRequest = {password};
        await apiClient.patch(`/reservation/${reservationId}/cancel`, request);
    },

    /**
     * 예약 목록 조회
     */
    list: async (): Promise<ReservationResponse[]> => {
        const response = await apiClient.get<ApiResponse<ReservationResponse[]>>('/reservation');
        return response.data;
    },

    /**
     * 예약 조회
     */
    get: async (reservationId: number): Promise<ReservationResponse> => {
        const response = await apiClient.get<ApiResponse<ReservationResponse>>(`/reservation/${reservationId}`);
        return response.data;
    },
};
