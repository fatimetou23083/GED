// src/app/shared/models/category.model.ts
export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id?: number;
  parent_name?: string;
  document_count: number;
  has_children: boolean;
  children?: Category[];
}