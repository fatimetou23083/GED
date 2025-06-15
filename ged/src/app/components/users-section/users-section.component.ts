// src/app/components/users-section/users-section.component.ts
import { Component, OnInit } from '@angular/core';
import { ApiService, User } from '../../api.service';

@Component({
  selector: 'app-users-section',
  templateUrl: './users-section.component.html',
  styleUrls: ['./users-section.component.css']
})
export class UsersSectionComponent implements OnInit {
  users: User[] = [];
  loading = false;
  error = '';
  selectedUser: User | null = null;
  showAddForm = false;
  
  // Formulaire pour nouvel utilisateur
  newUser = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
  };

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;
    this.error = '';
    
    this.apiService.getUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.loading = false;
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
        console.error('Erreur lors du chargement des utilisateurs:', error);
      }
    });
  }

  selectUser(user: User): void {
    this.selectedUser = user;
    this.showAddForm = false;
  }

  showAddUserForm(): void {
    this.showAddForm = true;
    this.selectedUser = null;
    this.resetNewUser();
  }

  resetNewUser(): void {
    this.newUser = {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: ''
    };
  }

  addUser(): void {
    if (!this.newUser.username || !this.newUser.email) {
      this.error = 'Nom d\'utilisateur et email sont requis';
      return;
    }

    this.loading = true;
    this.apiService.createUser(this.newUser).subscribe({
      next: (user) => {
        this.users.push(user);
        this.showAddForm = false;
        this.resetNewUser();
        this.loading = false;
        this.error = '';
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  updateUser(): void {
    if (!this.selectedUser) return;

    this.loading = true;
    this.apiService.updateUser(this.selectedUser.id, this.selectedUser).subscribe({
      next: (updatedUser) => {
        const index = this.users.findIndex(u => u.id === updatedUser.id);
        if (index !== -1) {
          this.users[index] = updatedUser;
        }
        this.selectedUser = updatedUser;
        this.loading = false;
        this.error = '';
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  deleteUser(user: User): void {
    if (confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur ${user.username} ?`)) {
      this.loading = true;
      this.apiService.deleteUser(user.id).subscribe({
        next: () => {
          this.users = this.users.filter(u => u.id !== user.id);
          if (this.selectedUser?.id === user.id) {
            this.selectedUser = null;
          }
          this.loading = false;
          this.error = '';
        },
        error: (error) => {
          this.error = error.message;
          this.loading = false;
        }
      });
    }
  }

  cancelEdit(): void {
    this.selectedUser = null;
    this.showAddForm = false;
    this.resetNewUser();
  }
}