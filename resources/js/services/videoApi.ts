import axios from 'axios';

export type VideoStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface VideoResource {
    id: number;
    status: VideoStatus;
    original_path: string;
    processed_path: string | null;
    created_at: string;
    updated_at: string;
}

export interface VideoResultResource {
    id: number;
    status: VideoStatus;
    processed_url: string | null;
}

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    headers: {
        Accept: 'application/json',
    },
});

export const uploadVideo = async (
    file: File,
    onProgress?: (progress: number) => void,
): Promise<VideoResource> => {
    const formData = new FormData();
    formData.append('video', file);

    const response = await api.post<VideoResource>('/videos', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (event) => {
            if (!event.total || !onProgress) {
                return;
            }

            const progress = Math.round((event.loaded / event.total) * 100);
            onProgress(progress);
        },
    });

    return response.data;
};

export const getVideoStatus = async (id: number): Promise<VideoResource> => {
    const response = await api.get<VideoResource>(`/videos/${id}`);

    return response.data;
};

export const getVideoResult = async (id: number): Promise<VideoResultResource> => {
    const response = await api.get<VideoResultResource>(`/videos/${id}/result`);

    return response.data;
};
