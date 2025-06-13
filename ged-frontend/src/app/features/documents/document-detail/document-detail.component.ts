// 📁 document-detail.component.ts - Version corrigée pour afficher et interagir avec un document
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DocumentService } from '../../../core/services/document.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-document-detail',
  templateUrl: './document-detail.component.html',
  styleUrls: ['./document-detail.component.scss']
})
export class DocumentDetailComponent implements OnInit {
  documentId: number = 0;
  document: any;
  versions: any[] = [];
  metadata: any[] = [];
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private documentService: DocumentService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.documentId = Number(this.route.snapshot.paramMap.get('id'));
    if (!this.documentId || isNaN(this.documentId)) {
      this.snackBar.open('ID de document invalide', 'Fermer', { duration: 3000 });
      this.router.navigate(['/documents']);
      return;
    }

    this.loadDocument();
    this.loadVersions();
    this.loadMetadata();
  }

  loadDocument(): void {
    this.loading = true;
    this.documentService.getDocumentById(this.documentId).subscribe({
      next: (doc) => {
        this.document = doc;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.snackBar.open('Document non trouvé', 'Fermer', { duration: 3000 });
        this.router.navigate(['/documents']);
      }
    });
  }

  loadVersions(): void {
    this.documentService.getDocumentVersions(this.documentId).subscribe({
      next: (data) => {
        this.versions = data;
      }
    });
  }

  loadMetadata(): void {
    this.documentService.getDocumentMetadata(this.documentId).subscribe({
      next: (data) => {
        this.metadata = data;
      }
    });
  }

  downloadVersion(versionId: number): void {
  this.documentService.downloadVersion(versionId).subscribe(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `version_${versionId}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
  }, error => {
    console.error('Erreur lors du téléchargement :', error);
  });
}


  goBack(): void {
    this.router.navigate(['/documents']);
  }
}
