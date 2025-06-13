export interface DocumentVersion {
  id: number;
  documentId: number;
  versionNumber: number;
  fileUrl: string;
  createdAt: Date;
  createdBy: number;
  comment?: string;
} 