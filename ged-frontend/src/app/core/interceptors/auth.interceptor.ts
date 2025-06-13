// src/app/core/interceptors/auth.interceptor.ts - VERSION CORRIGÉE
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    
    if (token) {
      let headers: { [name: string]: string } = {
        'Authorization': `Token ${token}`
      };

      // 🔥 CRUCIAL: Ne JAMAIS ajouter Content-Type pour FormData
      // Le navigateur doit définir automatiquement Content-Type avec boundary
      if (!(req.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
      }

      const authReq = req.clone({
        setHeaders: headers
      });
      
      console.log('🔗 Requête interceptée:', {
        url: authReq.url,
        method: authReq.method,
        headers: authReq.headers.keys(),
        isFormData: req.body instanceof FormData
      });
      
      return next.handle(authReq);
    }
    
    return next.handle(req);
  }
}
