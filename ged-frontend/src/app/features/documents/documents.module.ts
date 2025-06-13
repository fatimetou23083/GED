// documents.module.ts - VERSION CORRIGÉE
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

// Angular Material Modules
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatMenuModule } from '@angular/material/menu';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatDialogModule } from '@angular/material/dialog';

// Components
import { DocumentListComponent } from './document-list/document-list.component';
import { DocumentDetailComponent } from './document-detail/document-detail.component';
import { DocumentUploadComponent } from './document-upload/document-upload.component';
// Ne PAS importer ConfirmDialogComponent ici !

// Routing
import { DocumentsRoutingModule } from './documents-routing.module';

@NgModule({
  declarations: [
    DocumentListComponent,
    DocumentDetailComponent,
    DocumentUploadComponent
    // ConfirmDialogComponent a été retiré d'ici
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    DocumentsRoutingModule,
    
    // Angular Material
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatSnackBarModule,
    MatMenuModule,
    MatTooltipModule,
    MatTabsModule,
    MatDividerModule,
    MatDialogModule
  ]
})
export class DocumentsModule { }