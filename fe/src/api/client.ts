const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export class ApiError extends Error {
    constructor(
        public status: number,
        public statusText: string,
        message: string
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        throw new ApiError(
            response.status,
            response.statusText,
            errorText || `HTTP ${response.status}: ${response.statusText}`
        );
    }

    return response.json();
}

export const apiClient = {
    get: async <T>(path: string): Promise<T> => {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return handleResponse<T>(response);
    },

    post: async <T, D = unknown>(path: string, data: D): Promise<T> => {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        return handleResponse<T>(response);
    },

    put: async <T, D = unknown>(path: string, data: D): Promise<T> => {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        return handleResponse<T>(response);
    },

    delete: async <T>(path: string): Promise<T> => {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return handleResponse<T>(response);
    },
};
