export interface ApiResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  message?: string;
  status: 'success' | 'error';
} 