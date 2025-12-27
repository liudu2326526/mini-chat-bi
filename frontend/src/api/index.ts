import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
});

export interface UploadResponse {
  id: number;
  filename: string;
  columns: string[];
  preview: Record<string, any>[];
  created_at: string;
}

export const uploadFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export interface ChatRequest {
  file_id: number;
  query: string;
}

export interface ChatResponse {
  type: 'text' | 'chart' | 'error';
  content: string;
  options?: Record<string, any>;
}

export const sendChat = async (data: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/chat', data);
  return response.data;
};

export default api;
