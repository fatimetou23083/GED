
// workflows-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-workflows-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">⚙️ Workflows et Automatisation</h2>
        <p class="text-lg text-gray-600">
          Les workflows automatisent les processus métier en orchestrant les actions 
          sur vos documents selon des règles prédéfinies.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="space-y-6">
          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-orange-900 mb-4">🔄 Types de Workflows</h3>
            <div class="space-y-4">
              <div *ngFor="let workflow of workflowTypes" class="border-l-4 border-orange-500 pl-4">
                <h4 class="font-semibold text-gray-900">{{ workflow.name }}</h4>
                <p class="text-sm text-gray-600 mb-2">{{ workflow.description }}</p>
                <span class="inline-block text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">
                  {{ workflow.example }}
                </span>
              </div>
            </div>
          </div>

          <div class="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-green-900 mb-4">🎯 Déclencheurs</h3>
            <div class="space-y-2">
              <div *ngFor="let trigger of triggers" class="flex items-center gap-3">
                <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                <div>
                  <span class="font-medium text-green-900">{{ trigger.name }}</span>
                  <p class="text-xs text-green-700">{{ trigger.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-blue-900 mb-4">⚡ Actions Automatiques</h3>
            <div class="grid grid-cols-1 gap-3">
              <div *ngFor="let action of automaticActions" class="bg-white rounded-lg p-3 border">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-lg">{{ action.icon }}</span>
                  <span class="font-medium text-sm text-blue-900">{{ action.name }}</span>
                </div>
                <p class="text-xs text-blue-700">{{ action.description }}</p>
              </div>
            </div>
          </div>

          <div class="bg-purple-50 border border-purple-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-purple-900 mb-4">📊 Exemple Concret</h3>
            <div class="space-y-3">
              <div class="bg-white rounded-lg p-3 border-l-4 border-purple-500">
                <h4 class="font-semibold text-purple-900 mb-2">Validation de Facture</h4>
                <div class="space-y-2 text-sm text-purple-800">
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                    <span>1. Réception facture → Classification automatique</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                    <span>2. Notification au responsable financier</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                    <span>3. Validation ou rejet avec commentaires</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                    <span>4. Archivage automatique après traitement</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class WorkflowsSectionComponent {
  workflowTypes = [
    {
      name: 'Validation séquentielle',
      description: 'Approbation par étapes successives',
      example: 'Demande congés → Manager → RH → Validation'
    },
    {
      name: 'Validation parallèle',
      description: 'Approbation simultanée par plusieurs personnes',
      example: 'Contrat → Juridique + Commercial + Direction'
    },
    {
      name: 'Workflow conditionnel',
      description: 'Processus variables selon les critères',
      example: 'Facture > 10k€ → Validation direction'
    }
  ];

  triggers = [
    { name: 'Upload document', description: 'Lors de l\'ajout d\'un nouveau fichier' },
    { name: 'Modification métadonnées', description: 'Changement d\'informations' },
    { name: 'Échéance temporelle', description: 'Date limite atteinte' },
    { name: 'Changement statut', description: 'Évolution du workflow' },
    { name: 'Action utilisateur', description: 'Validation/Rejet manuel' }
  ];

  automaticActions = [
    { name: 'Email', icon: '📧', description: 'Notification automatique' },
    { name: 'Classification', icon: '📂', description: 'Rangement dans cabinet' },
    { name: 'Conversion', icon: '🔄', description: 'Transformation format' },
    { name: 'Archive', icon: '📦', description: 'Stockage long terme' },
    { name: 'Signature', icon: '✍️', description: 'Signature électronique' },
    { name: 'Extraction', icon: '🔍', description: 'OCR et indexation' }
  ];
}