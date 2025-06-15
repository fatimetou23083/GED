// src/app/components/catalog-section/catalog-section.component.ts
import { Component, OnInit } from '@angular/core';
import { ApiService, Category } from '../../api.service';

@Component({
  selector: 'app-catalog-section',
  templateUrl: './catalog-section.component.html',
  styleUrls: ['./catalog-section.component.css']
})
export class CatalogSectionComponent implements OnInit {
  categories: Category[] = [];
  rootCategories: Category[] = [];
  selectedCategory: Category | null = null;
  loading = false;
  error = '';
  showAddForm = false;
  
  // Formulaire pour nouvelle catégorie
  newCategory = {
    name: '',
    description: '',
    parent_id: null as number | null
  };

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.loading = true;
    this.error = '';
    
    // Charger toutes les catégories
    this.apiService.getCategories().subscribe({
      next: (response: any) => {
        console.log('Réponse catégories brute:', response);
        
        // Gérer différents formats de réponse
        if (Array.isArray(response)) {
          this.categories = response;
        } else if (response && response.results && Array.isArray(response.results)) {
          this.categories = response.results;
        } else if (response && Array.isArray(response.data)) {
          this.categories = response.data;
        } else {
          console.error('Format de réponse inattendu:', response);
          this.categories = [];
        }
        
        // Filtrer les catégories racines
        this.rootCategories = this.categories.filter(cat => !cat.parent_id);
        
        this.loading = false;
        console.log('Catégories chargées:', this.categories);
        console.log('Catégories racines:', this.rootCategories);
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
        console.error('Erreur lors du chargement des catégories:', error);
      }
    });
  }

  selectCategory(category: Category): void {
    this.selectedCategory = { ...category };
    this.showAddForm = false;
  }

  showAddCategoryForm(): void {
    this.showAddForm = true;
    this.selectedCategory = null;
    this.resetNewCategory();
  }

  resetNewCategory(): void {
    this.newCategory = {
      name: '',
      description: '',
      parent_id: null
    };
  }

  addCategory(): void {
    if (!this.newCategory.name.trim()) {
      this.error = 'Le nom de la catégorie est requis';
      return;
    }

    this.loading = true;
    console.log('Création de catégorie:', this.newCategory);
    
    this.apiService.createCategory(this.newCategory).subscribe({
      next: (category) => {
        console.log('Catégorie créée:', category);
        this.categories.push(category);
        if (!category.parent_id) {
          this.rootCategories.push(category);
        }
        this.showAddForm = false;
        this.resetNewCategory();
        this.loading = false;
        this.error = '';
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
        console.error('Erreur création catégorie:', error);
      }
    });
  }

  updateCategory(): void {
    if (!this.selectedCategory) return;

    this.loading = true;
    this.apiService.updateCategory(this.selectedCategory.id, this.selectedCategory).subscribe({
      next: (updatedCategory) => {
        const index = this.categories.findIndex(c => c.id === updatedCategory.id);
        if (index !== -1) {
          this.categories[index] = updatedCategory;
        }
        
        const rootIndex = this.rootCategories.findIndex(c => c.id === updatedCategory.id);
        if (rootIndex !== -1) {
          this.rootCategories[rootIndex] = updatedCategory;
        }
        
        this.selectedCategory = updatedCategory;
        this.loading = false;
        this.error = '';
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  deleteCategory(category: Category): void {
    if (confirm(`Êtes-vous sûr de vouloir supprimer la catégorie "${category.name}" ?`)) {
      this.loading = true;
      this.apiService.deleteCategory(category.id).subscribe({
        next: () => {
          this.categories = this.categories.filter(c => c.id !== category.id);
          this.rootCategories = this.rootCategories.filter(c => c.id !== category.id);
          if (this.selectedCategory?.id === category.id) {
            this.selectedCategory = null;
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

  getSubcategories(parentId: number): Category[] {
    return this.categories.filter(cat => cat.parent_id === parentId);
  }

  getParentName(parentId: number | null): string {
    if (!parentId) return 'Aucun parent';
    const parent = this.categories.find(cat => cat.id === parentId);
    return parent ? parent.name : 'Parent inconnu';
  }

  cancelEdit(): void {
    this.selectedCategory = null;
    this.showAddForm = false;
    this.resetNewCategory();
  }

  // Méthode pour exposer les catégories aux autres composants
  getAllCategories(): Category[] {
    return this.categories;
  }
}