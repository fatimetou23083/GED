// src/app/features/dashboard/dashboard.component.ts - VERSION MISE À JOUR
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { DocumentService } from '../../../core/services/document.service';
import { CategoryService } from '../../../core/services/category.service';
import { UserService } from '../../../core/services/user.service';

// Interfaces pour le dashboard
interface DashboardStats {
  documents: number;
  categories: number;
  users: number;
  recentDocuments: number;
}

interface RecentDocument {
  id: number;
  title: string;
  created_at: string;
  creator_name: string;
  status: string;
}

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_superuser?: boolean;
}

interface Category {
  id: number;
  name: string;
  description: string;
  document_count?: number;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  sidenavOpened = true;
  currentUser: any;
  loading = false;
  
  // Statistiques consolidées
  stats: DashboardStats = {
    documents: 0,
    categories: 0,
    users: 0,
    recentDocuments: 0
  };

  // Documents récents (les 5 derniers)
  recentDocuments: RecentDocument[] = [];

  // Utilisateurs récents
  users: User[] = [];

  // Catégories avec compteurs
  categories: Category[] = [];

  // Activité récente
  recentActivities: Array<{
    type: 'document' | 'user' | 'category';
    action: string;
    item: string;
    date: string;
    user: string;
  }> = [];

  constructor(
    private authService: AuthService,
    private documentService: DocumentService,
    private categoryService: CategoryService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUser();
    this.loadDashboardData();
  }

  /**
   * Charger toutes les données du dashboard
   */
  loadDashboardData(): void {
    this.loading = true;
    
    // Charger en parallèle
    Promise.all([
      this.loadDocumentStats(),
      this.loadUsers(),
      this.loadCategories(),
      this.loadRecentDocuments()
    ]).finally(() => {
      this.loading = false;
    });
  }

  /**
   * Charger les statistiques des documents
   */
  private loadDocumentStats(): Promise<void> {
    return new Promise((resolve) => {
      this.documentService.getDocuments().subscribe({
        next: (response: any) => {
          const documents = Array.isArray(response) ? response : 
                          (response.data || response.results || []);
          
          this.stats.documents = documents.length;
          this.stats.recentDocuments = documents.filter((doc: any) => {
            const daysSinceCreation = this.getDaysSince(doc.created_at);
            return daysSinceCreation <= 7; // Documents des 7 derniers jours
          }).length;
          
          resolve();
        },
        error: (error) => {
          console.error('Erreur documents:', error);
          resolve();
        }
      });
    });
  }

  /**
   * Charger les utilisateurs
   */
  private loadUsers(): Promise<void> {
    return new Promise((resolve) => {
      this.userService.getUsers().subscribe({
        next: (users: any) => {
          this.users = Array.isArray(users) ? users.slice(0, 5) : [];
          this.stats.users = Array.isArray(users) ? users.length : 0;
          resolve();
        },
        error: (error) => {
          console.error('Erreur utilisateurs:', error);
          this.users = [];
          resolve();
        }
      });
    });
  }

  /**
   * Charger les catégories
   */
  private loadCategories(): Promise<void> {
    return new Promise((resolve) => {
      this.categoryService.getCategories().subscribe({
        next: (categories: any) => {
          this.categories = Array.isArray(categories) ? categories : [];
          this.stats.categories = this.categories.length;
          resolve();
        },
        error: (error) => {
          console.error('Erreur catégories:', error);
          this.categories = [];
          resolve();
        }
      });
    });
  }

  /**
   * Charger les documents récents
   */
  private loadRecentDocuments(): Promise<void> {
    return new Promise((resolve) => {
      this.documentService.getDocuments().subscribe({
        next: (response: any) => {
          const documents = Array.isArray(response) ? response : 
                          (response.data || response.results || []);
          
          // Trier par date et prendre les 5 plus récents
          this.recentDocuments = documents
            .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
            .slice(0, 5)
            .map((doc: any) => ({
              id: doc.id,
              title: doc.title,
              created_at: doc.created_at,
              creator_name: doc.creator_name || 'Inconnu',
              status: doc.status
            }));
          
          resolve();
        },
        error: (error) => {
          console.error('Erreur documents récents:', error);
          this.recentDocuments = [];
          resolve();
        }
      });
    });
  }

  /**
   * Navigation vers la gestion des documents
   */
  goToDocuments(): void {
    this.router.navigate(['/documents']);
  }

  /**
   * Navigation vers l'upload de document
   */
  uploadDocument(): void {
    console.log('🚀 Navigation vers upload document');
    this.router.navigate(['/documents/create']);
  }


  /**
   * Voir un document spécifique
   */
  viewDocument(documentId: number): void {
    this.router.navigate(['/documents', documentId]);
  }

  /**
   * Navigation vers la gestion des utilisateurs
   */
  goToUsers(): void {
    this.router.navigate(['/users']);
  }

  /**
   * Navigation vers la gestion des catégories
   */
  goToCategories(): void {
    this.router.navigate(['/categories']);
  }

  /**
   * Basculer le sidenav
   */
  toggleSidenav(): void {
    this.sidenavOpened = !this.sidenavOpened;
  }

  /**
   * Déconnexion
   */
  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  /**
   * Actions pour les utilisateurs
   */
  editUser(user: User): void {
    this.router.navigate(['/users', user.id, 'edit']);
  }

  deleteUser(user: User): void {
    if (confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur ${user.username} ?`)) {
      this.userService.deleteUser(user.id).subscribe({
        next: () => {
          this.loadUsers();
        },
        error: (error) => console.error('Erreur suppression:', error)
      });
    }
  }

  toggleUserStatus(user: User): void {
    const newStatus = user.is_active ? 'INACTIF' : 'ACTIF';
    this.userService.updateUserStatus(user.id, newStatus as any).subscribe({
      next: () => {
        this.loadUsers();
      },
      error: (error) => console.error('Erreur changement statut:', error)
    });
  }

  /**
   * Obtenir le nombre de jours depuis une date
   */
  private getDaysSince(dateString: string): number {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  /**
   * Formater une date
   */
  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  /**
   * Obtenir la classe CSS pour le statut
   */
  getStatusClass(status: string): string {
    const statusClasses: { [key: string]: string } = {
      'DRAFT': 'status-draft',
      'PUBLISHED': 'status-published',
      'ARCHIVED': 'status-archived',
      'DELETED': 'status-deleted'
    };
    return statusClasses[status] || 'status-default';
  }

  /**
   * Obtenir le libellé du statut
   */
  getStatusLabel(status: string): string {
    const statusLabels: { [key: string]: string } = {
      'DRAFT': 'Brouillon',
      'PUBLISHED': 'Publié',
      'ARCHIVED': 'Archivé',
      'DELETED': 'Supprimé'
    };
    return statusLabels[status] || status;
  }

  /**
   * Actualiser toutes les données
   */
  refreshDashboard(): void {
    this.loadDashboardData();
  }
}