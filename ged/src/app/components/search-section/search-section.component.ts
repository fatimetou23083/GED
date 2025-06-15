
// 4. CRÉER search-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-search-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">🔍 Recherches Avancées</h2>
        <p class="text-lg text-gray-600">
          Moteur de recherche puissant pour retrouver rapidement vos documents.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-yellow-900 mb-4">🎯 Types de Recherche</h3>
          <div class="space-y-3">
            <div *ngFor="let type of searchTypes" class="border-l-4 border-yellow-500 pl-4">
              <h4 class="font-semibold">{{ type.name }}</h4>
              <p class="text-sm text-gray-600">{{ type.description }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-blue-900 mb-4">🔧 Fonctionnalités</h3>
          <div class="space-y-2">
            <div *ngFor="let feature of searchFeatures" class="flex items-center gap-2">
              <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
              <span class="text-sm">{{ feature }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class SearchSectionComponent {
  searchTypes = [
    { name: 'Recherche textuelle', description: 'Dans le contenu des documents OCR' },
    { name: 'Recherche par métadonnées', description: 'Filtres sur les champs personnalisés' },
    { name: 'Recherche combinée', description: 'Critères multiples avec opérateurs' }
  ];

  searchFeatures = [
    'Indexation automatique du contenu',
    'Recherche floue et approximative',
    'Filtres avancés par date, type, auteur',
    'Sauvegarde des recherches favorites'
  ];
}
