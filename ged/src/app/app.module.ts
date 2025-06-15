// 1. CORRIGER app.module.ts - Ajouter les routes manquantes
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { SummarySectionComponent } from './components/summary-section/summary-section.component';
import { CabinetsSectionComponent } from './components/cabinets-section/cabinets-section.component';
import { DocumentsSectionComponent } from './components/documents-section/documents-section.component';
import { MetadataSectionComponent } from './components/metadata-section/metadata-section.component';
import { PermissionsSectionComponent } from './components/permissions-section/permissions-section.component';
import { WorkflowsSectionComponent } from './components/workflows-section/workflows-section.component';
import { IndexComponent } from './pages/index/index.component';

// NOUVEAUX COMPOSANTS à créer
import { IndexSectionComponent } from './components/index-section/index-section.component';
import { TagsSectionComponent } from './components/tags-section/tags-section.component';
import { SearchSectionComponent } from './components/search-section/search-section.component';
import { MessagingSectionComponent } from './components/messaging-section/messaging-section.component';
import { SettingsSectionComponent } from './components/settings-section/settings-section.component';

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'summary', component: SummarySectionComponent },
  { path: 'documents', component: DocumentsSectionComponent },
  { path: 'cabinets', component: CabinetsSectionComponent },
  { path: 'metadata', component: MetadataSectionComponent },
  { path: 'index', component: IndexSectionComponent },
  { path: 'tags', component: TagsSectionComponent },
  { path: 'workflows', component: WorkflowsSectionComponent },
  { path: 'permissions', component: PermissionsSectionComponent },
  { path: 'search', component: SearchSectionComponent },
  { path: 'messaging', component: MessagingSectionComponent },
  { path: 'settings', component: SettingsSectionComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    SummarySectionComponent,
    CabinetsSectionComponent,
    DocumentsSectionComponent,
    MetadataSectionComponent,
    PermissionsSectionComponent,
    WorkflowsSectionComponent,
    IndexComponent,
    // NOUVEAUX COMPOSANTS
    IndexSectionComponent,
    TagsSectionComponent,
    SearchSectionComponent,
    MessagingSectionComponent,
    SettingsSectionComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
