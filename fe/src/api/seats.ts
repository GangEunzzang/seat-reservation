import {apiClient} from './client';
import type {ApiResponse} from './types';

export interface SeatCreateRequest {
    table_id: number;
    seat_number: number;
}

export interface SeatResponse {
    id: number;
    table_id: number;
    seat_number: number;
}

export const seatApi = {
    /**
     * 좌석 생성
     */
    create: async (request: SeatCreateRequest): Promise<SeatResponse> => {
        const response = await apiClient.post<ApiResponse<SeatResponse>>('/seat', request);
        return response.data;
    },

    /**
     * 좌석 조회
     */
    get: async (seatId: number): Promise<SeatResponse> => {
        const response = await apiClient.get<ApiResponse<SeatResponse>>(`/seat/${seatId}`);
        return response.data;
    },

    /**
     * 좌석 목록 조회
     */
    list: async (): Promise<SeatResponse[]> => {
        const response = await apiClient.get<ApiResponse<SeatResponse[]>>('/seat');
        return response.data;
    },

    /**
     * 좌석 삭제
     */
    delete: async (seatId: number): Promise<void> => {
        await apiClient.delete(`/seat/${seatId}`);
    },
};
