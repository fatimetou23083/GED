
// 2. CRÉER index-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-index-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">📚 Gestion des Index</h2>
        <p class="text-lg text-gray-600">
          Les index permettent de créer des vues dynamiques basées sur les métadonnées pour une navigation intuitive.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-orange-900 mb-4">📊 Index Dynamiques</h3>
          <div class="space-y-3">
            <div *ngFor="let index of dynamicIndexes" class="bg-orange-50 rounded-lg p-3">
              <h4 class="font-semibold text-orange-900">{{ index.name }}</h4>
              <p class="text-sm text-orange-700">{{ index.description }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-blue-900 mb-4">💡 Exemples</h3>
          <ul class="space-y-2">
            <li *ngFor="let example of examples" class="flex items-start gap-2">
              <span class="text-blue-600 mt-1">•</span>
              <span class="text-sm">{{ example }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class IndexSectionComponent {
  dynamicIndexes = [
    { name: 'Index par année', description: 'Classement chronologique automatique' },
    { name: 'Index par type', description: 'Regroupement par catégorie de document' },
    { name: 'Index par auteur', description: 'Organisation par créateur' }
  ];

  examples = [
    'Index "Par Année" → 2024 → Contrats, Factures',
    'Index "Par Département" → RH → Contrats emploi',
    'Index "Par Statut" → Validé → Documents approuvés'
  ];
}
