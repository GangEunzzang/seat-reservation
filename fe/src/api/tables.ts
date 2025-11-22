import {apiClient} from './client';
import type {ApiResponse} from './types';

export interface TableCreateRequest {
    episode_id: number;
    zone_id: number;
    x: number;
    y: number;
    name: string;
}

export interface TableUpdatePositionRequest {
    x: number;
    y: number;
}

export interface TableResponse {
    id: number;
    episode_id: number;
    zone_id: number;
    x: number;
    y: number;
    name: string;
}

export const tableApi = {
    /**
     * 테이블 생성
     */
    create: async (request: TableCreateRequest): Promise<TableResponse> => {
        const response = await apiClient.post<ApiResponse<TableResponse>>('/table', request);
        return response.data;
    },

    /**
     * 테이블 조회
     */
    get: async (tableId: number): Promise<TableResponse> => {
        const response = await apiClient.get<ApiResponse<TableResponse>>(`/table/${tableId}`);
        return response.data;
    },

    /**
     * 테이블 목록 조회
     */
    list: async (): Promise<TableResponse[]> => {
        const response = await apiClient.get<ApiResponse<TableResponse[]>>('/table');
        return response.data;
    },

    /**
     * 테이블 위치 수정
     */
    updatePosition: async (tableId: number, request: TableUpdatePositionRequest): Promise<TableResponse> => {
        const response = await apiClient.patch<ApiResponse<TableResponse>>(`/table/${tableId}/position`, request);
        return response.data;
    },

    /**
     * 테이블 삭제
     */
    delete: async (tableId: number): Promise<void> => {
        await apiClient.delete(`/table/${tableId}`);
    },
};
