import { Component } from '@angular/core';

@Component({
  selector: 'app-navigation',
  template: `
    <nav class="bg-white border border-gray-200 rounded-lg p-6 mb-8">
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
        <a 
          *ngFor="let item of navigationItems" 
          [routerLink]="item.path"
          routerLinkActive="bg-blue-600 text-white"
          class="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
          <div class="text-2xl">{{ item.icon }}</div>
          <div class="text-left">
            <div class="font-semibold text-sm">{{ item.title }}</div>
            <div class="text-xs text-gray-500">{{ item.subtitle }}</div>
          </div>
        </a>
      </div>
    </nav>
  `
})
export class NavigationComponent {
  navigationItems = [
    {
      title: 'Vue d\'ensemble',
      subtitle: 'Synthèse générale',
      icon: '📊',
      path: '/summary'
    },
    {
      title: 'Documents',
      subtitle: 'Gestion des fichiers',
      icon: '📄',
      path: '/documents'
    },
    {
      title: 'Cabinets',
      subtitle: 'Organisation',
      icon: '🗄️',
      path: '/cabinets'
    },
    {
      title: 'Métadonnées',
      subtitle: 'Types & Champs',
      icon: '🏷️',
      path: '/metadata'
    },
    {
      title: 'Permissions',
      subtitle: 'Sécurité & Accès',
      icon: '🔐',
      path: '/permissions'
    },
    {
      title: 'Workflows',
      subtitle: 'Automatisation',
      icon: '⚙️',
      path: '/workflows'
    },
    {
      title: 'Recherche',
      subtitle: 'Indexation',
      icon: '🔍',
      path: '/search'
    }
  ];
}