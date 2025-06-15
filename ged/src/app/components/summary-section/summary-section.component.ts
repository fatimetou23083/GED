// summary-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-summary-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">📊 Vue d'ensemble du système Mayan EDMS</h2>
        <p class="text-lg text-gray-600">
          Mayan EDMS est organisé en modules interconnectés qui travaillent ensemble pour offrir 
          une solution complète de gestion électronique de documents.
        </p>
      </div>

      <!-- Architecture Overview -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">🏗️ Architecture des Modules</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            *ngFor="let module of modules" 
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-center gap-3 mb-3">
              <div [ngClass]="'bg-' + module.color + '-100 p-2 rounded-lg'">
                <span class="text-2xl">{{ module.icon }}</span>
              </div>
              <h4 [ngClass]="'font-semibold text-' + module.color + '-900'">{{ module.name }}</h4>
            </div>
            <p class="text-sm text-gray-600 mb-3">{{ module.description }}</p>
            <div class="flex flex-wrap gap-1">
              <span 
                *ngFor="let feature of module.features" 
                class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                {{ feature }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature Matrix -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">🔄 Matrice des Fonctionnalités</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-2 font-semibold text-gray-900">Fonctionnalité</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Documents</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Cabinets</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Métadonnées</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Permissions</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Recherche</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Messages</th>
                <th class="text-center py-3 px-2 font-semibold text-gray-700">Paramètres</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let row of functionalityMatrix" class="border-b border-gray-100">
                <td class="py-3 px-2 font-medium text-gray-900">{{ row.functionality }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.documents }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.cabinets }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.metadata }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.permissions }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.search }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.messaging }}</td>
                <td class="px-2 py-3 text-center text-green-600 font-semibold">{{ row.settings }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="text-sm text-gray-500 mt-2">
          ✓ = Module impliqué dans cette fonctionnalité
        </p>
      </div>

      <!-- Implementation Workflow -->
      <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <h3 class="text-xl font-semibold text-blue-900 mb-4">🚀 Ordre de Mise en Œuvre Recommandé</h3>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div 
            *ngFor="let phase of implementationPhases; let i = index" 
            class="text-center">
            <div class="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center mx-auto mb-2 font-semibold">
              {{ i + 1 }}
            </div>
            <h4 class="font-semibold text-blue-900 mb-1">{{ phase.title }}</h4>
            <p class="text-xs text-blue-700">{{ phase.description }}</p>
          </div>
        </div>
      </div>
    </div>
  `
})
export class SummarySectionComponent {
  modules = [
    {
      name: 'Documents',
      icon: '📄',
      color: 'blue',
      description: 'Gestion centrale des fichiers, versions, et conversions',
      features: ['Upload', 'Versions', 'OCR', 'Conversion']
    },
    {
      name: 'Cabinets',
      icon: '🗄️',
      color: 'green',
      description: 'Organisation hiérarchique et classement logique',
      features: ['Arborescence', 'Classification', 'Organisation']
    },
    {
      name: 'Métadonnées',
      icon: '🏷️',
      color: 'purple',
      description: 'Types de documents et champs personnalisés',
      features: ['Types', 'Champs', 'Validation', 'Indexation']
    },
    {
      name: 'Permissions',
      icon: '🔐',
      color: 'red',
      description: 'Contrôle d\'accès granulaire et sécurité',
      features: ['Utilisateurs', 'Groupes', 'Rôles', 'ACL']
    },
    {
      name: 'Workflows',
      icon: '⚙️',
      color: 'orange',
      description: 'Automatisation des processus métier',
      features: ['États', 'Transitions', 'Actions', 'Conditions']
    },
    {
      name: 'Recherche',
      icon: '🔍',
      color: 'teal',
      description: 'Indexation avancée et recherche full-text',
      features: ['Full-text', 'Filtres', 'Index', 'Résultats']
    }
  ];

  functionalityMatrix = [
    {
      functionality: 'Stockage des fichiers',
      documents: '✓',
      cabinets: '-',
      metadata: '-',
      permissions: '✓',
      search: '-',
      messaging: '-',
      settings: '✓'
    },
    {
      functionality: 'Classification hiérarchique',
      documents: '✓',
      cabinets: '✓',
      metadata: '✓',
      permissions: '✓',
      search: '-',
      messaging: '-',
      settings: '-'
    },
    {
      functionality: 'Définition des types',
      documents: '✓',
      cabinets: '-',
      metadata: '✓',
      permissions: '-',
      search: '✓',
      messaging: '-',
      settings: '✓'
    },
    {
      functionality: 'Contrôle d\'accès',
      documents: '✓',
      cabinets: '✓',
      metadata: '✓',
      permissions: '✓',
      search: '✓',
      messaging: '✓',
      settings: '✓'
    },
    {
      functionality: 'Recherche et indexation',
      documents: '✓',
      cabinets: '✓',
      metadata: '✓',
      permissions: '✓',
      search: '✓',
      messaging: '-',
      settings: '✓'
    }
  ];

  implementationPhases = [
    { title: 'Paramétrage', description: 'Configuration de base' },
    { title: 'Types & Métadonnées', description: 'Structure documentaire' },
    { title: 'Permissions', description: 'Sécurité et accès' },
    { title: 'Documents & Cabinets', description: 'Organisation' },
    { title: 'Workflows & Recherche', description: 'Automatisation' }
  ];
}