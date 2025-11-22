import {apiClient} from './client';
import type {ApiResponse} from './types';

export interface EpisodeCreateRequest {
    year: number;
    name: string;
    start_date: string;
    end_date: string;
}

export interface EpisodeResponse {
    id: number;
    year: number;
    name: string;
    start_date: string;
    end_date: string;
}

export const episodeApi = {
    /**
     * 에피소드 생성
     */
    create: async (request: EpisodeCreateRequest): Promise<EpisodeResponse> => {
        const response = await apiClient.post<ApiResponse<EpisodeResponse>>('/episode', request);
        return response.data;
    },

    /**
     * 에피소드 조회
     */
    get: async (episodeId: number): Promise<EpisodeResponse> => {
        const response = await apiClient.get<ApiResponse<EpisodeResponse>>(`/episode/${episodeId}`);
        return response.data;
    },

    /**
     * 에피소드 목록 조회
     */
    list: async (): Promise<EpisodeResponse[]> => {
        const response = await apiClient.get<ApiResponse<EpisodeResponse[]>>('/episode');
        return response.data;
    },

    /**
     * 에피소드 삭제
     */
    delete: async (episodeId: number): Promise<void> => {
        await apiClient.delete(`/episode/${episodeId}`);
    },
};
