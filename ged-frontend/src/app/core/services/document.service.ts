// src/app/core/services/document.service.ts - VERSION CORRIGÉE FINALE
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

// Models
interface Document {
  id: number;
  title: string;
  description?: string;
  category_id: number;
  category_name?: string;
  creator_id: number;
  creator_name?: string;
  created_at: string;
  updated_at?: string;
  status: string;
  is_favorite?: boolean;
  is_deleted?: boolean;
  file_hash?: string;
}

interface DocumentVersion {
  id: number;
  document_id: number;
  version_number: number;
  file_path: string;
  created_at: string;
  created_by_id: number;
  creator_name?: string;
}

interface Metadata {
  id: number;
  document_id: number;
  key: string;
  value_type: string;
  value_text: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private baseUrl = `${environment.apiUrl}/documents`;

  constructor(private http: HttpClient) {
    console.log('📡 DocumentService initialized with baseUrl:', this.baseUrl);
  }

  // ✅ UPLOAD PRINCIPAL avec debug
  uploadDocument(formData: FormData): Observable<any> {
    console.log('📡 === SERVICE UPLOAD START ===');
    console.log('📡 URL cible:', `${this.baseUrl}/`);
    console.log('📡 Environment API URL:', environment.apiUrl);
    
    // Debug FormData
    // console.log('📦 FormData contents:');
    // for (let pair of formData.entries()) {
    //   if (pair[1] instanceof File) {
    //     console.log(`  ${pair[0]}: FILE - ${pair[1].name} (${pair[1].size} bytes)`);
    //   } else {
    //     console.log(`  ${pair[0]}: ${pair[1]}`);
    //   }
    // }
    
    const url = `${this.baseUrl}/`;
    console.log('📡 Final URL:', url);
    
    return this.http.post<any>(url, formData).pipe(
      tap(response => {
        console.log('✅ Service - Response received:', response);
      }),
      catchError(error => {
        console.error('❌ Service - Error caught:', error);
        return throwError(error);
      })
    );
  }

  // ✅ CRUD Operations
  getDocuments(): Observable<Document[]> {
    console.log('📡 GET Documents from:', `${this.baseUrl}/`);
    return this.http.get<Document[]>(`${this.baseUrl}/`).pipe(
      tap(docs => console.log('✅ Documents loaded:', docs.length)),
      catchError(error => {
        console.error('❌ Error loading documents:', error);
        return throwError(error);
      })
    );
  }

  getDocumentById(id: number): Observable<Document> {
    return this.http.get<Document>(`${this.baseUrl}/${id}/`);
  }

  createDocument(documentData: FormData): Observable<Document> {
    return this.uploadDocument(documentData);
  }

  updateDocument(id: number, documentData: FormData): Observable<Document> {
    return this.http.put<Document>(`${this.baseUrl}/${id}/`, documentData);
  }

  deleteDocument(id: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/${id}/supprimer/`, {});
  }

  // ✅ Downloads
  downloadDocument(id: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${id}/download_latest/`, {
      responseType: 'blob'
    });
  }

  downloadVersion(versionId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/versions/${versionId}/download/`, {
      responseType: 'blob'
    });
  }

  // ✅ Versions et métadonnées
  getDocumentVersions(documentId: number): Observable<DocumentVersion[]> {
    const params = new HttpParams().set('document_id', documentId.toString());
    return this.http.get<DocumentVersion[]>(`${this.baseUrl}/versions/by_document/`, { params });
  }

  getDocumentMetadata(documentId: number): Observable<Metadata[]> {
    const params = new HttpParams().set('document_id', documentId.toString());
    return this.http.get<Metadata[]>(`${this.baseUrl}/metadata/by_document/`, { params });
  }

  // ✅ Categories
  getCategories(): Observable<any[]> {
    const url = `${environment.apiUrl}/categories/`;
    console.log('📡 GET Categories from:', url);
    return this.http.get<any[]>(url).pipe(
      tap(cats => console.log('✅ Categories loaded:', cats.length)),
      catchError(error => {
        console.error('❌ Error loading categories:', error);
        return throwError(error);
      })
    );
  }

  // ✅ Other operations
  getFavoriteDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.baseUrl}/favoris/`);
  }

  getTrashDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.baseUrl}/corbeille/`);
  }

  toggleFavorite(id: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/${id}/toggle_favori/`, {});
  }

  restoreDocument(id: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/${id}/restaurer/`, {});
  }
}