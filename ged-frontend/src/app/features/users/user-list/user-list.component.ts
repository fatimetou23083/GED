import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {
  // Propriété pour le champ de recherche
  searchQuery: string = '';

  // Liste complète des utilisateurs
  allUsers: any[] = [
    { id: 1, fullName: 'John Doe', role: 'ADMIN', status: 'active', avatar: null },
    { id: 2, fullName: 'Jane Smith', role: 'USER', status: 'inactive', avatar: 'path/to/avatar.jpg' },
    // Ajoutez d'autres utilisateurs ici
  ];

  // Liste des utilisateurs affichés après filtrage
  filteredUsers: any[] = [];
  displayedUsers: any[] = [];

  // Propriétés de pagination
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalPages: number = 1;

  // Propriété pour le sidenav
  sidenavOpened: boolean = false;

  constructor() {}

  ngOnInit(): void {
    this.applyFilter(); // Initialiser le filtrage
  }

  // Méthode pour basculer le sidenav
  toggleSidenav(): void {
    this.sidenavOpened = !this.sidenavOpened;
  }

  // Méthode pour appliquer le filtre de recherche
  applyFilter(): void {
    this.filteredUsers = this.allUsers.filter(user =>
      user.fullName.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
    this.currentPage = 1;
    this.calculatePagination();
  }

  // Méthode pour calculer la pagination
  calculatePagination(): void {
    this.totalPages = Math.max(1, Math.ceil(this.filteredUsers.length / this.itemsPerPage));
    this.updateDisplayedUsers();
  }

  // Méthode pour mettre à jour les utilisateurs affichés en fonction de la page actuelle
  updateDisplayedUsers(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.displayedUsers = this.filteredUsers.slice(startIndex, endIndex);
  }

  // Méthode pour passer à la page précédente
  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updateDisplayedUsers();
    }
  }

  // Méthode pour passer à la page suivante
  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updateDisplayedUsers();
    }
  }

  // Méthode pour nettoyer les classes dynamiques
  sanitizeClass(value: string): string {
    return value.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
  }

  // Méthode pour obtenir les initiales d'un utilisateur
  getUserInitials(user: any): string {
    if (!user.fullName) {
      return '??';
    }
    return user.fullName
      .split(' ')
      .map((name: string) => name.charAt(0))
      .join('')
      .toUpperCase()
      .substring(0, 2);
  }

  // Méthode pour ajouter un utilisateur (exemple)
  addUser(): void {
    alert('Ajouter un utilisateur - Fonctionnalité à implémenter');
  }

  // Méthode pour éditer un utilisateur (exemple)
  editUser(user: any): void {
    alert(`Modifier l'utilisateur : ${user.fullName} - Fonctionnalité à implémenter`);
  }

  // Méthode pour supprimer un utilisateur (exemple)
  deleteUser(user: any): void {
    alert(`Supprimer l'utilisateur : ${user.fullName} - Fonctionnalité à implémenter`);
  }

  // Méthode pour se déconnecter (exemple)
  logout(): void {
    alert('Déconnexion - Fonctionnalité à implémenter');
  }
}