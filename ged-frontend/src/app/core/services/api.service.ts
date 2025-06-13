// src/app/core/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  constructor(private http: HttpClient) {}

  /**
   * GET request
   */
  get<T>(endpoint: string, params?: any): Observable<T> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key].toString());
        }
      });
    }

    return this.http.get<T>(`${environment.apiUrl}${endpoint}`, { params: httpParams });
  }

  /**
   * POST request
   */
  post<T>(endpoint: string, body: any): Observable<T> {
    return this.http.post<T>(`${environment.apiUrl}${endpoint}`, body);
  }

  /**
   * PUT request
   */
  put<T>(endpoint: string, body: any): Observable<T> {
    return this.http.put<T>(`${environment.apiUrl}${endpoint}`, body);
  }

  /**
   * PATCH request
   */
  patch<T>(endpoint: string, body: any): Observable<T> {
    return this.http.patch<T>(`${environment.apiUrl}${endpoint}`, body);
  }

  /**
   * DELETE request
   */
  delete<T>(endpoint: string): Observable<T> {
  return this.http.delete<T>(`${environment.apiUrl}${endpoint}`);
}

  /**
   * Upload de fichier
   */
  uploadFile<T>(endpoint: string, formData: FormData): Observable<T> {
    return this.http.post<T>(`${environment.apiUrl}${endpoint}`, formData);
  }

  /**
   * Télécharger un fichier
   */
  downloadFile(endpoint: string): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}${endpoint}`, {
      responseType: 'blob'
    });
  }

  /**
   * Construire l'URL complète pour les médias
   */
  getMediaUrl(path: string): string {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return `${environment.mediaUrl}/${path}`;
  }
}