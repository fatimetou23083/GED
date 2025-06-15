// src/app/components/cabinets-section/cabinets-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-cabinets-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">🗄️ Cabinets et Organisation</h2>
        <p class="text-lg text-gray-600">
          Les cabinets permettent d'organiser vos documents de manière hiérarchique et logique, 
          créant une structure claire pour votre système documentaire.
        </p>
      </div>

      <!-- Structure hiérarchique -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">🏗️ Structure Hiérarchique</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div *ngFor="let level of hierarchyLevels" class="border border-gray-200 rounded-lg p-4">
            <div class="flex items-center gap-3 mb-3">
              <span class="text-2xl">{{ level.icon }}</span>
              <h4 class="font-semibold text-gray-900">{{ level.name }}</h4>
            </div>
            <p class="text-sm text-gray-600 mb-3">{{ level.description }}</p>
            <div class="space-y-1">
              <div *ngFor="let example of level.examples" class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                {{ example }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Fonctionnalités -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">⚙️ Fonctionnalités des Cabinets</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div *ngFor="let feature of cabinetFeatures" class="border border-gray-200 rounded-lg p-4">
            <div class="bg-blue-100 p-3 rounded-lg mb-3">
              <span class="text-2xl">{{ feature.icon }}</span>
            </div>
            <h4 class="font-semibold text-blue-900 mb-2">{{ feature.title }}</h4>
            <p class="text-sm text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </div>

      <!-- Règles de classement -->
      <div class="bg-white border border-gray-200 rounded-lg p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">📋 Règles de Classement Automatique</h3>
        <div class="space-y-4">
          <div *ngFor="let rule of classificationRules" class="border-l-4 border-green-500 pl-4">
            <h4 class="font-semibold text-gray-900">{{ rule.name }}</h4>
            <p class="text-sm text-gray-600 mb-2">{{ rule.description }}</p>
            <div class="flex flex-wrap gap-2">
              <span *ngFor="let criteria of rule.criteria" 
                    class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                {{ criteria }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class CabinetsSectionComponent {
  hierarchyLevels = [
    {
      name: 'Cabinet Principal',
      icon: '🏛️',
      description: 'Niveau racine de l\'organisation',
      examples: ['Direction Générale', 'Ressources Humaines', 'Comptabilité']
    },
    {
      name: 'Sous-Cabinet',
      icon: '📁',
      description: 'Divisions thématiques ou départementales',
      examples: ['Contrats', 'Factures', 'Rapports', 'Correspondances']
    },
    {
      name: 'Dossiers',
      icon: '📂',
      description: 'Regroupement par projet ou période',
      examples: ['2024', 'Projet Alpha', 'Client XYZ', 'Formation']
    },
    {
      name: 'Sous-Dossiers',
      icon: '📄',
      description: 'Organisation fine des documents',
      examples: ['Originaux', 'Copies', 'Brouillons', 'Validés']
    }
  ];

  cabinetFeatures = [
    {
      title: 'Navigation Intuitive',
      icon: '🧭',
      description: 'Interface arborescente pour parcourir facilement la structure documentaire'
    },
    {
      title: 'Permissions Héritées',
      icon: '🔐',
      description: 'Droits d\'accès transmis automatiquement dans la hiérarchie'
    },
    {
      title: 'Recherche Contextuelle',
      icon: '🔍',
      description: 'Filtrage des résultats par emplacement dans l\'arborescence'
    },
    {
      title: 'Statistiques Visuelles',
      icon: '📊',
      description: 'Aperçu du nombre de documents par cabinet et sous-cabinet'
    },
    {
      title: 'Glisser-Déposer',
      icon: '↔️',
      description: 'Déplacement simple des documents entre les emplacements'
    },
    {
      title: 'Favoris et Raccourcis',
      icon: '⭐',
      description: 'Accès rapide aux cabinets les plus utilisés'
    }
  ];

  classificationRules = [
    {
      name: 'Classement par Type de Document',
      description: 'Redirection automatique selon le type détecté',
      criteria: ['Type MIME', 'Extension fichier', 'Métadonnées document']
    },
    {
      name: 'Classement par Date',
      description: 'Organisation chronologique automatique',
      criteria: ['Date création', 'Date modification', 'Période extraite du contenu']
    },
    {
      name: 'Classement par Contenu',
      description: 'Analyse du texte pour déterminer la destination',
      criteria: ['Mots-clés détectés', 'Entités nommées', 'Classification ML']
    },
    {
      name: 'Classement par Source',
      description: 'Destination selon l\'origine du document',
      criteria: ['Email expéditeur', 'Scanner utilisé', 'Application source']
    }
  ];
}