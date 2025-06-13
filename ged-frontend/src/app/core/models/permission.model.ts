export interface Permission {
  id: number;
  documentId: number;
  userId: number;
  type: 'READ' | 'WRITE' | 'ADMIN';
  grantedAt: Date;
  grantedBy: number;
} 