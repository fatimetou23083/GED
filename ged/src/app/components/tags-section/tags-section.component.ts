
// 3. CRÉER tags-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-tags-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">🏷️ Système de Tags</h2>
        <p class="text-lg text-gray-600">
          Les tags offrent une classification flexible avec des étiquettes colorées pour vos documents.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-pink-900 mb-4">🎨 Tags Colorés</h3>
          <div class="space-y-3">
            <div *ngFor="let tag of colorTags" class="flex items-center gap-3">
              <span [ngClass]="'w-4 h-4 rounded-full ' + tag.color"></span>
              <span class="font-medium">{{ tag.name }}</span>
              <span class="text-sm text-gray-500">{{ tag.usage }}</span>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-blue-900 mb-4">⚡ Avantages</h3>
          <ul class="space-y-2">
            <li *ngFor="let benefit of benefits" class="flex items-start gap-2">
              <span class="text-green-600 mt-1">•</span>
              <span class="text-sm">{{ benefit }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class TagsSectionComponent {
  colorTags = [
    { name: 'Urgent', color: 'bg-red-500', usage: 'Documents prioritaires' },
    { name: 'Validé', color: 'bg-green-500', usage: 'Documents approuvés' },
    { name: 'En cours', color: 'bg-yellow-500', usage: 'Traitement en cours' }
  ];

  benefits = [
    'Classification rapide et visuelle',
    'Recherche par tags multiples',
    'Filtrage instantané des documents',
    'Organisation personnalisable'
  ];
}
