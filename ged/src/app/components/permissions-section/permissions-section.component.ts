
// permissions-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-permissions-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">🔐 Gestion des Permissions</h2>
        <p class="text-lg text-gray-600">
          Le système de permissions garantit la sécurité et contrôle l'accès aux documents 
          selon les rôles et responsabilités de chaque utilisateur.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="space-y-6">
          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-red-900 mb-4">👥 Gestion des Utilisateurs</h3>
            <div class="space-y-4">
              <div *ngFor="let userLevel of userLevels" class="border-l-4 border-red-500 pl-4">
                <h4 class="font-semibold text-gray-900">{{ userLevel.name }}</h4>
                <p class="text-sm text-gray-600 mb-2">{{ userLevel.description }}</p>
                <div class="flex flex-wrap gap-1">
                  <span *ngFor="let permission of userLevel.permissions" 
                        class="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                    {{ permission }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-blue-900 mb-4">🏢 Groupes d'Utilisateurs</h3>
            <div class="space-y-3">
              <div *ngFor="let group of userGroups" class="bg-blue-50 rounded-lg p-3">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-blue-600">{{ group.icon }}</span>
                  <h4 class="font-semibold text-blue-900">{{ group.name }}</h4>
                </div>
                <p class="text-sm text-blue-700">{{ group.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-gray-900 mb-4">⚡ Types d'Actions</h3>
            <div class="grid grid-cols-2 gap-3">
              <div *ngFor="let action of permissionActions" class="bg-white rounded-lg p-3 border">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-lg">{{ action.icon }}</span>
                  <span class="font-medium text-sm text-gray-900">{{ action.name }}</span>
                </div>
                <p class="text-xs text-gray-600">{{ action.description }}</p>
              </div>
            </div>
          </div>

          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 class="text-xl font-semibold text-yellow-900 mb-4">🎯 Bonnes Pratiques</h3>
            <ul class="space-y-2">
              <li *ngFor="let practice of bestPractices" class="flex items-start gap-2">
                <span class="text-yellow-600 mt-1">•</span>
                <p class="text-sm text-yellow-800">{{ practice }}</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  `
})
export class PermissionsSectionComponent {
  userLevels = [
    {
      name: 'Administrateur',
      description: 'Accès complet au système',
      permissions: ['Créer', 'Lire', 'Modifier', 'Supprimer', 'Gérer permissions']
    },
    {
      name: 'Gestionnaire',
      description: 'Gestion des documents de son service',
      permissions: ['Créer', 'Lire', 'Modifier', 'Valider']
    },
    {
      name: 'Utilisateur',
      description: 'Consultation et création limitée',
      permissions: ['Lire', 'Créer (limité)']
    },
    {
      name: 'Invité',
      description: 'Accès en lecture seule',
      permissions: ['Lire (limité)']
    }
  ];

  userGroups = [
    {
      name: 'Direction',
      icon: '👔',
      description: 'Accès privilégié aux documents stratégiques'
    },
    {
      name: 'Ressources Humaines',
      icon: '👥',
      description: 'Gestion des documents RH et confidentiels'
    },
    {
      name: 'Comptabilité',
      icon: '💰',
      description: 'Documents financiers et facturations'
    },
    {
      name: 'Commercial',
      icon: '📈',
      description: 'Contrats clients et propositions'
    }
  ];

  permissionActions = [
    { name: 'Voir', icon: '👁️', description: 'Consulter le document' },
    { name: 'Télécharger', icon: '⬇️', description: 'Sauvegarder localement' },
    { name: 'Modifier', icon: '✏️', description: 'Éditer le contenu' },
    { name: 'Supprimer', icon: '🗑️', description: 'Effacer définitivement' },
    { name: 'Partager', icon: '🔗', description: 'Donner accès à d\'autres' },
    { name: 'Commenter', icon: '💬', description: 'Ajouter des annotations' }
  ];

  bestPractices = [
    'Appliquez le principe du moindre privilège',
    'Révisez régulièrement les permissions accordées',
    'Utilisez les groupes plutôt que des permissions individuelles',
    'Documentez les rôles et responsabilités',
    'Activez la journalisation des accès',
    'Formez les utilisateurs aux bonnes pratiques de sécurité'
  ];
}
