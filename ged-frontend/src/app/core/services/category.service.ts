// src/app/core/services/category.service.ts - REMPLACER ENTIÈREMENT
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  constructor(private http: HttpClient) {}

  getCategories(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/categories/`);
  }

  getCategoryById(id: number): Observable<any> {
    return this.http.get(`${environment.apiUrl}/categories/${id}/`);
  }

  createCategory(category: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/categories/`, category);
  }

  updateCategory(id: number, category: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/categories/${id}/`, category);
  }

  deleteCategory(id: number): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/categories/${id}/`);
  }
}