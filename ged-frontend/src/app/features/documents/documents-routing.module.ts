//  Créer le fichier : src/app/features/documents/documents-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DocumentListComponent } from './document-list/document-list.component';
import { DocumentDetailComponent } from './document-detail/document-detail.component';
import { DocumentUploadComponent } from './document-upload/document-upload.component';
import { AuthGuard } from '../../core/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: DocumentListComponent
  },
  {
    path: 'create',
    component: DocumentUploadComponent
  },
  {
    path: ':id',
    component: DocumentDetailComponent
  },
  {
    path: ':id/edit',
    component: DocumentUploadComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DocumentsRoutingModule { }