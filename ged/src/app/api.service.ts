// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

// Interfaces basées sur votre backend existant
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile?: {
    phone: string;
    address: string;
    avatar: string;
  };
}

export interface Document {
  id: number;
  title: string;
  description: string;
  file_path: string;
  created_at: string;
  updated_at: string;
  category?: any;
  creator?: User;
  is_deleted: boolean;
}

export interface Cabinet {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id: number | null;
  children?: Category[];
}

export interface Workflow {
  id: number;
  name: string;
  description: string;
  is_active: boolean;
  created_by: User;
}

export interface AuthResponse {
  token: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api'; // Changé pour localhost
  private tokenSubject = new BehaviorSubject<string | null>(localStorage.getItem('token'));
  public token$ = this.tokenSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Headers avec authentification
  private getHeaders(): HttpHeaders {
    const token = this.tokenSubject.value;
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': token ? `Token ${token}` : ''
    });
  }

  // Gestion des erreurs
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Une erreur est survenue';
    if (error.error instanceof ErrorEvent) {
      errorMessage = error.error.message;
    } else {
      errorMessage = `Erreur ${error.status}: ${error.message}`;
    }
    console.error('Erreur API:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }

  // AUTHENTIFICATION - utilise votre endpoint existant
  login(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/users/auth/login/`, {
      username,
      password
    }).pipe(
      tap(response => {
        localStorage.setItem('token', response.token);
        this.tokenSubject.next(response.token);
      }),
      catchError(this.handleError)
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    this.tokenSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!this.tokenSubject.value;
  }

  // UTILISATEURS - utilise vos endpoints users/users/ existants
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/users/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/users/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  createUser(user: Partial<User>): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/users/users/`, user, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateUser(id: number, user: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/users/${id}/`, user, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/users/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  searchUsers(query: string): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/users/search/?q=${encodeURIComponent(query)}`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // PROFIL UTILISATEUR
  getMyProfile(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/users/profiles/my_profile/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // DOCUMENTS - utilise vos endpoints documents/documents/ existants
  getDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/documents/documents/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getAllDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/documents/documents/all/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getDocument(id: number): Observable<Document> {
    return this.http.get<Document>(`${this.apiUrl}/documents/documents/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  createDocument(document: Partial<Document>): Observable<Document> {
    return this.http.post<Document>(`${this.apiUrl}/documents/documents/`, document, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateDocument(id: number, document: Partial<Document>): Observable<Document> {
    return this.http.put<Document>(`${this.apiUrl}/documents/documents/${id}/`, document, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  deleteDocument(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/documents/documents/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  searchDocuments(query: string): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/documents/documents/search/?q=${encodeURIComponent(query)}`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // CABINETS - utilise vos endpoints cabinets/cabinets/ existants  
  getCabinets(): Observable<Cabinet[]> {
    return this.http.get<Cabinet[]>(`${this.apiUrl}/cabinets/cabinets/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getCabinet(id: number): Observable<Cabinet> {
    return this.http.get<Cabinet>(`${this.apiUrl}/cabinets/cabinets/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  createCabinet(cabinet: Partial<Cabinet>): Observable<Cabinet> {
    return this.http.post<Cabinet>(`${this.apiUrl}/cabinets/cabinets/`, cabinet, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateCabinet(id: number, cabinet: Partial<Cabinet>): Observable<Cabinet> {
    return this.http.put<Cabinet>(`${this.apiUrl}/cabinets/cabinets/${id}/`, cabinet, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  deleteCabinet(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/cabinets/cabinets/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // CATEGORIES - utilise vos endpoints catalog/categories/ existants
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/catalog/categories/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getRootCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/catalog/categories/root_categories/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getCategoryTree(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/catalog/categories/tree/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  createCategory(category: Partial<Category>): Observable<Category> {
    return this.http.post<Category>(`${this.apiUrl}/catalog/categories/`, category, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateCategory(id: number, category: Partial<Category>): Observable<Category> {
    return this.http.put<Category>(`${this.apiUrl}/catalog/categories/${id}/`, category, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/catalog/categories/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // WORKFLOWS - utilise vos endpoints workflows/definitions/ existants
  getWorkflows(): Observable<Workflow[]> {
    return this.http.get<Workflow[]>(`${this.apiUrl}/workflows/definitions/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getWorkflow(id: number): Observable<Workflow> {
    return this.http.get<Workflow>(`${this.apiUrl}/workflows/definitions/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  createWorkflow(workflow: Partial<Workflow>): Observable<Workflow> {
    return this.http.post<Workflow>(`${this.apiUrl}/workflows/definitions/`, workflow, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateWorkflow(id: number, workflow: Partial<Workflow>): Observable<Workflow> {
    return this.http.put<Workflow>(`${this.apiUrl}/workflows/definitions/${id}/`, workflow, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  deleteWorkflow(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/workflows/definitions/${id}/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getWorkflowStates(workflowId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/workflows/definitions/${workflowId}/states/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // UPLOAD DE FICHIERS - CORRIGÉ selon votre backend
  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', file.name);
    formData.append('category_id', '1'); // Vous devrez adapter selon vos catégories
    
    const token = this.tokenSubject.value;
    const headers = new HttpHeaders({
      'Authorization': token ? `Token ${token}` : ''
      // Ne pas définir Content-Type pour FormData
    });

    // Utilise directement l'endpoint create du DocumentViewSet
    return this.http.post(`${this.apiUrl}/documents/documents/`, formData, {
      headers: headers
    }).pipe(catchError(this.handleError));
  }

  // Version alternative simplifiée pour créer un document sans fichier
  createDocumentOnly(document: Partial<Document>): Observable<Document> {
    return this.http.post<Document>(`${this.apiUrl}/documents/documents/`, document, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  

  // PERMISSIONS
  getPermissions(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/permissions/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // TAGS/TAGGER
  getTags(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/tags/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // COMMENTAIRES
  getComments(documentId?: number): Observable<any[]> {
    const url = documentId 
      ? `${this.apiUrl}/comments/?document_id=${documentId}`
      : `${this.apiUrl}/comments/`;
    
    return this.http.get<any[]>(url, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // MESSAGING
  getMessages(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/messaging/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // INDEXING - utilise vos endpoints indexing/ existants
  getIndexes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/indexing/queue/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getIndexingJobs(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/indexing/jobs/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getIndexingStats(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/indexing/stats/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  reindexAllDocuments(): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/indexing/reindex-all/`, {}, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  // SETTINGS - utilise vos endpoints settings/ existants
  getSettings(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/settings/system/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getCurrentSettings(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/settings/system/current/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getUserPreferences(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/settings/preferences/my/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  updateUserPreferences(preferences: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/settings/preferences/my/`, preferences, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }

  getPublicSettings(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/settings/application/public/`, {
      headers: this.getHeaders()
    }).pipe(catchError(this.handleError));
  }
  
// MÉTADONNÉES - section complète
getMetadataTypes(): Observable<any[]> {
  return this.http.get<any[]>(`${this.apiUrl}/metadata/types/`, {
    headers: this.getHeaders()
  }).pipe(catchError(this.handleError));
}

createMetadataType(metadata: any): Observable<any> {
  return this.http.post<any>(`${this.apiUrl}/metadata/types/`, metadata, {
    headers: this.getHeaders()
  }).pipe(catchError(this.handleError));
}

updateMetadataType(id: number, metadata: any): Observable<any> {
  return this.http.put<any>(`${this.apiUrl}/metadata/types/${id}/`, metadata, {
    headers: this.getHeaders()
  }).pipe(catchError(this.handleError));
}

deleteMetadataType(id: number): Observable<void> {
  return this.http.delete<void>(`${this.apiUrl}/metadata/types/${id}/`, {
    headers: this.getHeaders()
  }).pipe(catchError(this.handleError));
}
}
