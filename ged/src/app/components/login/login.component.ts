// Alternative login.component.ts SANS ngModel
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  error = '';

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  // Gestion des inputs sans ngModel
  onUsernameChange(event: any): void {
    this.username = event.target.value;
  }

  onPasswordChange(event: any): void {
    this.password = event.target.value;
  }

  onSubmit(): void {
    if (!this.username || !this.password) {
      this.error = 'Nom d\'utilisateur et mot de passe requis';
      return;
    }

    this.loading = true;
    this.error = '';

    this.apiService.login(this.username, this.password).subscribe({
      next: (response) => {
        console.log('Connexion réussie:', response);
        this.loading = false;
        this.router.navigate(['/']); // Rediriger vers la page d'accueil
      },
      error: (error) => {
        this.error = 'Nom d\'utilisateur ou mot de passe incorrect';
        this.loading = false;
        console.error('Erreur de connexion:', error);
      }
    });
  }
}
