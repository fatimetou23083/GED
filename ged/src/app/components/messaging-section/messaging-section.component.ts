
// 5. CRÉER messaging-section.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-messaging-section',
  template: `
    <div class="max-w-4xl mx-auto p-6">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">💬 Système de Messagerie</h2>
        <p class="text-lg text-gray-600">
          Communication intégrée pour la collaboration sur les documents.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-cyan-900 mb-4">📧 Types de Messages</h3>
          <div class="space-y-3">
            <div *ngFor="let type of messageTypes" class="bg-cyan-50 rounded-lg p-3">
              <h4 class="font-semibold text-cyan-900">{{ type.name }}</h4>
              <p class="text-sm text-cyan-700">{{ type.description }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="text-xl font-semibold text-green-900 mb-4">🔔 Notifications</h3>
          <ul class="space-y-2">
            <li *ngFor="let notification of notifications" class="flex items-start gap-2">
              <span class="text-green-600 mt-1">•</span>
              <span class="text-sm">{{ notification }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class MessagingSectionComponent {
  messageTypes = [
    { name: 'Messages internes', description: 'Communication entre utilisateurs du système' },
    { name: 'Notifications automatiques', description: 'Alertes générées par les workflows' },
    { name: 'Commentaires sur documents', description: 'Annotations collaboratives' }
  ];

  notifications = [
    'Nouveau document ajouté',
    'Validation requise',
    'Échéance approchante',
    'Modification de permissions'
  ];
}
