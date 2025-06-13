// src/app/features/documents/document-upload/document-upload.component.ts - VERSION COMPLÈTE
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { DocumentService } from '../../../core/services/document.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-document-upload',
  templateUrl: './document-upload.component.html',
  styleUrls: ['./document-upload.component.scss']
})
export class DocumentUploadComponent implements OnInit {
  uploadForm!: FormGroup;
  selectedFile: File | null = null;
  categories: any[] = [];
  uploading: boolean = false;
  uploadProgress: number = 0;

  // ✅ Types de fichiers autorisés
  private allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'image/jpeg',
    'image/jpg',
    'image/png'
  ];

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private router: Router,
    private documentService: DocumentService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadCategories();
  }

  // ✅ Initialisation du formulaire
  private initForm(): void {
    this.uploadForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      description: [''],
      category_id: ['', Validators.required],
      status: ['DRAFT']
    });
  }

  // ✅ Charger les catégories
  private loadCategories(): void {
    this.documentService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        console.log('✅ Catégories chargées:', categories);
      },
      error: (error) => {
        console.error('❌ Erreur chargement catégories:', error);
        this.snackBar.open('❌ Erreur chargement catégories', 'Fermer', { duration: 3000 });
      }
    });
  }

  // ✅ Ouvrir le sélecteur de fichier
  openFileDialog(): void {
    const input = document.getElementById('fileInput') as HTMLInputElement;
    if (input) {
      input.click();
    }
  }

  // ✅ Gestion de la sélection de fichier COMPLÈTE
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) {
      return;
    }

    const file = input.files[0];
    console.log('📁 Fichier sélectionné:', {
      name: file.name,
      size: file.size,
      type: file.type
    });

    // ✅ Validation de la taille (50MB max)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
      this.snackBar.open('❌ Fichier trop volumineux (max 50MB)', 'Fermer', { duration: 4000 });
      this.resetFileInput();
      return;
    }

    // ✅ Validation du type MIME
    if (!this.allowedTypes.includes(file.type)) {
      this.snackBar.open(`❌ Type de fichier non supporté: ${file.type}`, 'Fermer', { duration: 4000 });
      this.resetFileInput();
      return;
    }

    // ✅ Fichier valide
    this.selectedFile = file;
    console.log('✅ Fichier accepté');
  }

  // ✅ Reset du fichier sélectionné
  resetFileInput(): void {
    const input = document.getElementById('fileInput') as HTMLInputElement;
    if (input) {
      input.value = '';
    }
    this.selectedFile = null;
  }

  // ✅ Formatage taille fichier
  formatFileSize(size: number): string {
    if (size === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(size) / Math.log(k));
    return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // ✅ Icône du fichier
  getFileIcon(filename: string): string {
    const ext = filename.split('.').pop()?.toLowerCase();
    const iconMap: { [key: string]: string } = {
      'pdf': 'picture_as_pdf',
      'doc': 'description',
      'docx': 'description',
      'xls': 'table_chart',
      'xlsx': 'table_chart',
      'ppt': 'slideshow',
      'pptx': 'slideshow',
      'jpg': 'image',
      'jpeg': 'image',
      'png': 'image'
    };
    return iconMap[ext || ''] || 'insert_drive_file';
  }

  // ✅ Vérification avant upload
  canUpload(): boolean {
    return this.uploadForm.valid && !!this.selectedFile;
  }

 // ✅ REMPLACEZ UNIQUEMENT la méthode uploadDocument() dans document-upload.component.ts
uploadDocument(): void {
  console.log('🚀 === DÉBUT DEBUG UPLOAD ===');
  
  // 1. Vérifications de base
  console.log('📋 Form valid:', this.uploadForm.valid);
  console.log('📁 File selected:', !!this.selectedFile);
  console.log('📝 Form values:', this.uploadForm.value);
  
  if (!this.uploadForm.valid || !this.selectedFile) {
    console.error('❌ Validation échouée');
    this.snackBar.open("❌ Formulaire invalide ou fichier manquant", "Fermer", { duration: 4000 });
    return;
  }

  // 2. Informations sur le fichier
  console.log('📎 Fichier détails:', {
    name: this.selectedFile.name,
    size: this.selectedFile.size,
    type: this.selectedFile.type,
    lastModified: new Date(this.selectedFile.lastModified)
  });

  // 3. Création FormData avec logs
  const formData = new FormData();
  formData.append('title', this.uploadForm.value.title);
  formData.append('description', this.uploadForm.value.description || '');
  formData.append('category_id', this.uploadForm.value.category_id);
  formData.append('status', this.uploadForm.value.status || 'DRAFT');
  formData.append('file', this.selectedFile);

  // 4. Vérification FormData
  // console.log('📦 FormData créé:');
  // for (let pair of formData.entries()) {
  //   if (pair[1] instanceof File) {
  //     console.log(`${pair[0]}: FILE - ${pair[1].name} (${pair[1].size} bytes)`);
  //   } else {
  //     console.log(`${pair[0]}: ${pair[1]}`);
  //   }
  // }

  // 5. URL et headers
  console.log('📡 URL cible:', `${environment.apiUrl}/documents/`);
  
  this.uploading = true;

  // 6. Appel HTTP avec debug complet
  this.documentService.uploadDocument(formData).subscribe({
    next: (response) => {
      console.log("✅ === SUCCESS ===");
      console.log("✅ Réponse complète:", response);
      console.log("✅ Type de réponse:", typeof response);
      console.log("✅ ID du document:", response?.id);
      
      this.uploading = false;
      this.snackBar.open("✅ Document uploadé avec succès", "Fermer", { duration: 3000 });
      
      // Navigation
      if (response && response.id) {
        console.log("📍 Navigation vers:", `/documents/${response.id}`);
        this.router.navigate(['/documents', response.id]);
      } else {
        console.log("📍 Navigation vers: /documents");
        this.router.navigate(['/documents']);
      }
    },
    error: (error) => {
      console.error("❌ === ERROR COMPLET ===");
      console.error("❌ Status:", error.status);
      console.error("❌ Status Text:", error.statusText);
      console.error("❌ URL:", error.url);
      console.error("❌ Error Object:", error.error);
      console.error("❌ Message:", error.message);
      console.error("❌ Headers:", error.headers);
      
      this.uploading = false;
      
      // Messages d'erreur détaillés
      let errorMessage = "❌ Erreur lors de l'upload";
      
      if (error.status === 0) {
        errorMessage = "❌ Impossible de contacter le serveur Django";
        console.error("🔍 Vérifiez que Django tourne sur http://localhost:8000");
      } else if (error.status === 400) {
        errorMessage = `❌ Erreur 400: ${error.error?.error || 'Données invalides'}`;
      } else if (error.status === 401) {
        errorMessage = "❌ Non autorisé - Problème d'authentification";
      } else if (error.status === 403) {
        errorMessage = "❌ Accès interdit";
      } else if (error.status === 404) {
        errorMessage = "❌ URL non trouvée - Vérifiez les routes Django";
      } else if (error.status === 413) {
        errorMessage = "❌ Fichier trop volumineux";
      } else if (error.status === 500) {
        errorMessage = "❌ Erreur serveur Django";
      }
      
      console.error("📢 Message utilisateur:", errorMessage);
      this.snackBar.open(errorMessage, "Fermer", { duration: 5000 });
    }
  });
  
  console.log('🚀 === REQUÊTE ENVOYÉE ===');
}

  // ✅ Marquer tous les champs comme touchés pour afficher les erreurs
  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  // ✅ Navigation
  cancel(): void {
    this.router.navigate(['/documents']);
  }

  // ✅ Reset complet du formulaire
  resetForm(): void {
    this.uploadForm.reset({
      status: 'DRAFT'
    });
    this.resetFileInput();
  }
}