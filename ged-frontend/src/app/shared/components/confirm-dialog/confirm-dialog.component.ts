// confirm-dialog.component.ts - VERSION CORRIGÉE
import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface ConfirmDialogData {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
}

@Component({
  selector: 'app-confirm-dialog',
  template: `
    <h1 mat-dialog-title>{{ data.title }}</h1>
    <div mat-dialog-content>
      <p [innerHTML]="formatMessage(data.message)"></p>
    </div>
    <div mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">
        {{ data.cancelText || 'Annuler' }}
      </button>
      <button mat-raised-button color="warn" (click)="onConfirm()">
        {{ data.confirmText || 'Confirmer' }}
      </button>
    </div>
  `,
  styles: [`
    mat-dialog-actions {
      justify-content: flex-end;
      gap: 8px;
      padding: 16px 24px;
    }
    
    mat-dialog-content p {
      margin: 16px 0;
      line-height: 1.5;
    }
    
    mat-dialog-title {
      margin-bottom: 0;
    }
  `]
})
export class ConfirmDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ConfirmDialogData
  ) {}

  onConfirm(): void {
    this.dialogRef.close(true);
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  // Méthode pour formater le message avec des sauts de ligne
  formatMessage(message: string): string {
    return message.replace(/\n/g, '<br>');
  }
}