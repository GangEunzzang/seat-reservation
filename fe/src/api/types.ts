export interface ApiResponse<T> {
    success: boolean;
    data: T;
    message: string;
}

export interface UserRegisterRequest {
    name: string;
    department: string;
    position: string;
    phone_number: string;
    episode_id: number;
}

export interface UserResponse {
    id: number;
    name: string;
    department: string;
    position: string;
    phone_number: string;
    episode_id: number;
    created_at: string;
    updated_at: string;
}
