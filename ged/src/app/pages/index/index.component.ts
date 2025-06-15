import { Component } from '@angular/core';

@Component({
  selector: 'app-index',
  template: `
    <div class="text-center py-12">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">
        Bienvenue dans la documentation du système GED
      </h2>
      <p class="text-lg text-gray-600 mb-8">
        Explorez les différents modules pour comprendre le fonctionnement du système.
      </p>
      <div class="max-w-2xl mx-auto">
        <app-summary-section></app-summary-section>
      </div>
    </div>
  `
})
export class IndexComponent { }