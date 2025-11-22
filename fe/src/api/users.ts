import {apiClient} from './client';
import type {ApiResponse, UserRegisterRequest, UserResponse} from './types';

export const userApi = {
    register: (request: UserRegisterRequest) =>
        apiClient.post<ApiResponse<UserResponse>>('/user', request),

    registerBulk: (requests: UserRegisterRequest[]) =>
        apiClient.post<ApiResponse<UserResponse[]>>('/user/bulk', requests),

    getById: (userId: number) =>
        apiClient.get<ApiResponse<UserResponse>>(`/user/${userId}`),

    list: () =>
        apiClient.get<ApiResponse<UserResponse[]>>('/user'),

    delete: (userId: number) =>
        apiClient.delete<void>(`/user/${userId}`),
};
