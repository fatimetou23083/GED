// app.component.ts - Version améliorée
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Guide Mayan EDMS';
  
  // État de la sidebar (ouvert par défaut)
  sidebarOpen = true;

  // Fonction pour basculer l'état de la sidebar avec animation fluide
  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
    
    // Petit feedback haptic sur mobile (si supporté)
    if ('vibrate' in navigator) {
      navigator.vibrate(50);
    }
  }

  // Fermer la sidebar sur mobile quand on clique sur un lien
  closeSidebarOnMobile() {
    if (window.innerWidth <= 768) {
      this.sidebarOpen = false;
    }
  }

  // Getter pour le texte du bouton toggle
  get toggleButtonText(): string {
    return this.sidebarOpen ? 'Fermer' : 'Menu';
  }

  // Getter pour l'aria-label du bouton
  get toggleButtonAriaLabel(): string {
    return this.sidebarOpen ? 'Fermer le menu de navigation' : 'Ouvrir le menu de navigation';
  }
}