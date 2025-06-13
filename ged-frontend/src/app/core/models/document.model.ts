export interface Document {
  id: number;
  title: string;
  description?: string;
  fileUrl: string;
  categoryId: number;
  creatorId: number;
  createdAt: Date;
  updatedAt?: Date;
  creator?: {
    id: number;
    name: string;
  };
} 