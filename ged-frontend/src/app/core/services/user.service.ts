// Allez dans : src/app/core/services/user.service.ts
// Remplacez TOUT le contenu par :

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  
  constructor(private http: HttpClient) {}

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/users/`);
  }

  getUserById(id: number): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}/users/${id}/`);
  }

  createUser(user: any): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}/users/`, user);
  }

  updateUser(id: number, user: any): Observable<any> {
    return this.http.put<any>(`${environment.apiUrl}/users/${id}/`, user);
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/users/${id}/`);
  }

  updateUserStatus(id: number, status: string): Observable<any> {
    return this.http.patch<any>(`${environment.apiUrl}/users/${id}/`, { status });
  }
}