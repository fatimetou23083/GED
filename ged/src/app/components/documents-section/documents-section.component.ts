import { Component } from '@angular/core';

@Component({
  selector: 'app-documents-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">📄 Gestion des Documents</h2>
        <p class="text-lg text-gray-600">
          Le module Documents est le cœur de Mayan EDMS, gérant le stockage, les versions, 
          les conversions et toutes les opérations sur vos fichiers.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-blue-900 mb-4">📤 Upload & Import</h3>
          <p class="text-gray-600 mb-4">Importation de documents avec support multi-formats</p>
          <ul class="space-y-1">
            <li class="text-sm text-gray-600">• Drag & drop</li>
            <li class="text-sm text-gray-600">• Upload par lots</li>
            <li class="text-sm text-gray-600">• Importation email</li>
            <li class="text-sm text-gray-600">• API REST</li>
          </ul>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-green-900 mb-4">📝 Gestion des Versions</h3>
          <p class="text-gray-600 mb-4">Suivi complet des modifications et historique</p>
          <ul class="space-y-1">
            <li class="text-sm text-gray-600">• Versions automatiques</li>
            <li class="text-sm text-gray-600">• Historique complet</li>
            <li class="text-sm text-gray-600">• Comparaison</li>
            <li class="text-sm text-gray-600">• Rollback</li>
          </ul>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-purple-900 mb-4">🔄 Transformation</h3>
          <p class="text-gray-600 mb-4">Conversion automatique entre formats</p>
          <ul class="space-y-1">
            <li class="text-sm text-gray-600">• PDF/A</li>
            <li class="text-sm text-gray-600">• Compression</li>
            <li class="text-sm text-gray-600">• Extraction texte</li>
            <li class="text-sm text-gray-600">• Génération aperçus</li>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class DocumentsSectionComponent { }