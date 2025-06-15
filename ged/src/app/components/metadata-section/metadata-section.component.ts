// metadata-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-metadata-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">🏷️ Gestion des Métadonnées</h2>
        <p class="text-lg text-gray-600">
          Les métadonnées enrichissent vos documents avec des informations structurées, 
          facilitant leur classification, recherche et gestion automatisée.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div class="space-y-6">
          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-purple-900 mb-4">📋 Types de Métadonnées</h3>
            <p class="text-gray-600 mb-4">Définissez les différents types selon vos besoins métier</p>
            <ul class="space-y-2">
              <li *ngFor="let type of metadataTypes" class="flex items-center gap-2">
                <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
                <span class="text-sm text-gray-700">{{ type.name }} - {{ type.description }}</span>
              </li>
            </ul>
          </div>

          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-green-900 mb-4">🎯 Champs Personnalisés</h3>
            <div class="space-y-3">
              <div *ngFor="let field of customFields" class="border-l-4 border-green-500 pl-4">
                <h4 class="font-semibold text-gray-900">{{ field.type }}</h4>
                <p class="text-sm text-gray-600">{{ field.description }}</p>
                <span class="inline-block text-xs bg-green-100 text-green-800 px-2 py-1 rounded mt-1">
                  {{ field.example }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-purple-50 border border-purple-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-purple-900 mb-4">⚙️ Configuration</h3>
            <div class="space-y-4">
              <div *ngFor="let config of configurations" class="bg-white rounded-lg p-4 border">
                <div class="flex items-center gap-3 mb-2">
                  <span class="text-2xl">{{ config.icon }}</span>
                  <h4 class="font-semibold text-gray-900">{{ config.title }}</h4>
                </div>
                <p class="text-sm text-gray-600">{{ config.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class MetadataSectionComponent {
  metadataTypes = [
    { name: 'Matière', description: 'Classification thématique' },
    { name: 'Année', description: 'Période temporelle' },
    { name: 'Auteur', description: 'Créateur du document' },
    { name: 'Statut', description: 'État du document' },
    { name: 'Priorité', description: 'Niveau d\'importance' }
  ];

  customFields = [
    {
      type: 'Texte libre',
      description: 'Champs textuels pour informations diverses',
      example: 'Nom du client, référence projet'
    },
    {
      type: 'Liste de choix',
      description: 'Valeurs prédéfinies dans un menu déroulant',
      example: 'Urgent/Normal/Faible, Validé/En cours/Rejeté'
    },
    {
      type: 'Date',
      description: 'Champs temporels avec calendrier',
      example: 'Date de création, échéance'
    },
    {
      type: 'Numérique',
      description: 'Valeurs numériques avec validation',
      example: 'Montant, quantité, pourcentage'
    }
  ];

  configurations = [
    {
      icon: '✅',
      title: 'Validation',
      description: 'Règles de contrôle des données saisies'
    },
    {
      icon: '🔒',
      title: 'Obligatoire',
      description: 'Champs requis lors de l\'indexation'
    },
    {
      icon: '🔄',
      title: 'Héritage',
      description: 'Transmission automatique entre versions'
    }
  ];
}
