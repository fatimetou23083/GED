// src/app/shared/models/api-response.model.ts
export interface ApiResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface ApiError {
  error: string;
  details?: any;
}