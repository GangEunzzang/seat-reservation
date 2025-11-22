import {apiClient} from './client';
import type {ApiResponse} from './types';

export interface ZoneCreateRequest {
    episode_id: number;
    code: string;
    name: string;
}

export interface ZoneUpdateRequest {
    name: string;
}

export interface ZoneResponse {
    id: number;
    episode_id: number;
    code: string;
    name: string;
}

export const zoneApi = {
    /**
     * Zone 생성
     */
    create: async (request: ZoneCreateRequest): Promise<ZoneResponse> => {
        const response = await apiClient.post<ApiResponse<ZoneResponse>>('/zone', request);
        return response.data;
    },

    /**
     * Zone 조회
     */
    get: async (zoneId: number): Promise<ZoneResponse> => {
        const response = await apiClient.get<ApiResponse<ZoneResponse>>(`/zone/${zoneId}`);
        return response.data;
    },

    /**
     * Episode의 Zone 목록 조회
     */
    listByEpisode: async (episodeId: number): Promise<ZoneResponse[]> => {
        const response = await apiClient.get<ApiResponse<ZoneResponse[]>>(`/zone/episode/${episodeId}`);
        return response.data;
    },

    /**
     * Zone 이름 수정
     */
    update: async (zoneId: number, request: ZoneUpdateRequest): Promise<ZoneResponse> => {
        const response = await apiClient.patch<ApiResponse<ZoneResponse>>(`/zone/${zoneId}`, request);
        return response.data;
    },

    /**
     * Zone 삭제
     */
    delete: async (zoneId: number): Promise<void> => {
        await apiClient.delete(`/zone/${zoneId}`);
    },
};
