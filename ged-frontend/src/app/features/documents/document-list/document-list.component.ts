// 📁 document-list.component.ts - FONCTION DOWNLOAD & IMPORTATION CORRIGÉES
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { DocumentService } from '../../../core/services/document.service';

@Component({
  selector: 'app-document-list',
  templateUrl: './document-list.component.html',
  styleUrls: ['./document-list.component.scss']
})
export class DocumentListComponent implements OnInit {
  documents: any[] = [];
  filteredDocuments: any[] = [];
  categories: any[] = [];
  statusOptions = [
    { value: 'DRAFT', label: 'Brouillon' },
    { value: 'PUBLISHED', label: 'Publié' },
    { value: 'ARCHIVED', label: 'Archivé' }
  ];

  searchQuery = '';
  selectedCategory: number | undefined = undefined;
  selectedStatus: string | undefined = undefined;

  viewMode: string = 'active';
  loading = false;

  displayedColumns: string[] = ['title', 'category', 'creator', 'created_at', 'actions'];
  itemsPerPage = 10;
  currentPage = 1;

  constructor(
    private documentService: DocumentService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (history.state.uploaded) {
      this.snackBar.open('✅ Document uploadé avec succès', 'Fermer', { duration: 3000 });
    }
    this.fetchDocuments();
    this.fetchCategories();
  }

  fetchDocuments(): void {
    this.loading = true;
    this.documentService.getDocuments().subscribe({
      next: (docs) => {
        this.documents = docs;
        this.applyFilters();
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.snackBar.open('❌ Erreur lors du chargement des documents', 'Fermer', { duration: 3000 });
      }
    });
  }

  fetchCategories(): void {
    this.documentService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      }
    });
  }

  getPageTitle(): string {
    switch (this.viewMode) {
      case 'active': return 'Documents actifs';
      case 'favorites': return 'Documents favoris';
      case 'trash': return 'Corbeille';
      case 'duplicates': return 'Documents en doublon';
      default: return 'Documents';
    }
  }

  getPageIcon(): string {
    switch (this.viewMode) {
      case 'active': return 'folder';
      case 'favorites': return 'star';
      case 'trash': return 'delete';
      case 'duplicates': return 'content_copy';
      default: return 'insert_drive_file';
    }
  }

  setViewMode(mode: string): void {
    this.viewMode = mode;
    this.applyFilters();
  }

  onSearchChange(): void { this.applyFilters(); }
  onCategoryChange(): void { this.applyFilters(); }
  onStatusChange(): void { this.applyFilters(); }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = undefined;
    this.selectedStatus = undefined;
    this.applyFilters();
  }

  applyFilters(): void {
    this.filteredDocuments = this.documents.filter(doc => {
      const queryMatch = this.searchQuery ?
        (doc.title?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        doc.creator_name?.toLowerCase().includes(this.searchQuery.toLowerCase())) : true;

      const categoryMatch = this.selectedCategory ? doc.category_id === this.selectedCategory : true;

      const statusMatch = this.selectedStatus ? doc.status === this.selectedStatus : true;

      return queryMatch && categoryMatch && statusMatch;
    });
    this.currentPage = 1;
  }

  getCategoryName(categoryId: number): string {
    const category = this.categories.find(c => c.id === categoryId);
    return category ? category.name : 'Inconnue';
  }

  viewDocument(document: any): void {
    this.router.navigate(['/documents', document.id]);
  }

  deleteDocument(document: any): void {
    if (confirm(`Supprimer le document « ${document.title} » ?`)) {
      this.documentService.deleteDocument(document.id).subscribe({
        next: () => {
          this.snackBar.open('Document supprimé', 'Fermer', { duration: 2000 });
          this.fetchDocuments();
        },
        error: () => {
          this.snackBar.open('Erreur suppression', 'Fermer', { duration: 2000 });
        }
      });
    }
  }

  emptyTrash(): void {
    if (confirm('Voulez-vous vraiment vider la corbeille ?')) {
      this.documents = this.documents.filter(doc => doc.status !== 'trash');
      this.applyFilters();
    }
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString();
  }

  getPaginatedDocuments(): any[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredDocuments.slice(start, start + this.itemsPerPage);
  }

  getTotalPages(): number {
    return Math.ceil(this.filteredDocuments.length / this.itemsPerPage);
  }

  nextPage(): void { if (this.currentPage < this.getTotalPages()) this.currentPage++; }
  previousPage(): void { if (this.currentPage > 1) this.currentPage--; }

  createDocument(): void {
    this.router.navigate(['/documents/upload']);
  }

  // ✅ Téléchargement corrigé
  downloadLatest(docId: number): void {
    this.documentService.downloadDocument(docId).subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `document_${docId}.pdf`;
      a.click();
    });
  }

}
