// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';
  private tokenKey = 'auth_token';
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Vérifier si un token existe au démarrage
    this.loadCurrentUser();
  }

  // Connexion utilisateur
  login(credentials: { username: string; password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/auth/login/`, credentials)
      .pipe(
        tap((response: any) => {
          if (response.token) {
            localStorage.setItem(this.tokenKey, response.token);
            this.currentUserSubject.next(response.user);
            console.log('✅ Connexion réussie:', response.user);
          }
        })
      );
  }

  // Inscription utilisateur
  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/auth/register/`, userData)
      .pipe(
        tap((response: any) => {
          if (response.token) {
            localStorage.setItem(this.tokenKey, response.token);
            this.currentUserSubject.next(response.user);
            console.log('✅ Inscription réussie:', response.user);
          }
        })
      );
  }

  // Déconnexion
  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.currentUserSubject.next(null);
    console.log('✅ Déconnexion effectuée');
  }

  // Vérifier si l'utilisateur est connecté
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  // Récupérer le token
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  // Récupérer l'utilisateur actuel
  getCurrentUser(): any {
    return this.currentUserSubject.value;
  }

  // Charger l'utilisateur actuel depuis le localStorage
  private loadCurrentUser(): void {
    const token = this.getToken();
    if (token) {
      // Optionnel: récupérer les infos utilisateur depuis l'API
      this.getUserProfile().subscribe({
        next: (user) => this.currentUserSubject.next(user),
        error: () => this.logout() // Token invalide
      });
    }
  }

  // Récupérer le profil utilisateur
  private getUserProfile(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Token ${this.getToken()}`
    });
    return this.http.get(`${this.apiUrl}/users/profile/`, { headers });
  }

  // Obtenir les headers avec authentification
  getAuthHeaders(): HttpHeaders {
    const token = this.getToken();
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': token ? `Token ${token}` : ''
    });
  }
}