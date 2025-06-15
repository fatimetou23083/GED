
// 6. CRÉER settings-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-settings-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">⚙️ Paramétrage Système</h2>
        <p class="text-lg text-gray-600">
          Configuration globale et personnalisation de Mayan EDMS.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">🔧 Configuration Générale</h3>
          <div class="space-y-3">
            <div *ngFor="let config of generalSettings" class="border-l-4 border-gray-500 pl-4">
              <h4 class="font-semibold">{{ config.name }}</h4>
              <p class="text-sm text-gray-600">{{ config.description }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-purple-900 mb-4">👤 Préférences Utilisateur</h3>
          <div class="space-y-2">
            <div *ngFor="let pref of userPreferences" class="flex items-center gap-2">
              <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
              <span class="text-sm">{{ pref }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class SettingsSectionComponent {
  generalSettings = [
    { name: 'Paramètres de stockage', description: 'Configuration des espaces de stockage' },
    { name: 'Formats supportés', description: 'Types de fichiers autorisés' },
    { name: 'Sécurité globale', description: 'Politiques de sécurité système' }
  ];

  userPreferences = [
    'Interface utilisateur personnalisée',
    'Notifications par email',
    'Langue de l\'interface',
    'Fuseau horaire'
  ];
}