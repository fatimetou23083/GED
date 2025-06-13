// src/app/shared/models/document.model.ts
export interface Document {
  id: number;
  title: string;
  description: string;
  category_id: number;
  category_name: string;
  creator_id: number;
  creator_name: string;
  created_at: string;
  status: string;
  versions?: DocumentVersion[];
  metadata?: Metadata[];
  comments?: Comment[];
  tags?: Tag[];
  permissions?: Permission[];
}

export interface DocumentVersion {
  id: number;
  document_id: number;
  version_number: number;
  file_path: string;
  created_at: string;
  created_by_id: number;
  creator_name: string;
}

export interface Metadata {
  id: number;
  document_id: number;
  key: string;
  value_type: string;
  value_text: string;
}

export interface Comment {
  id: number;
  document_id: number;
  author_id: number;
  author_name: string;
  content: string;
  created_at: string;
  parent_id?: number;
  has_replies: boolean;
  replies?: Comment[];
}

export interface Tag {
  id: number;
  name: string;
  color: string;
  document_count?: number;
}

export interface Permission {
  id: number;
  document_id: number;
  document_title: string;
  user_id: number;
  user_name: string;
  permission_type: 'READ' | 'WRITE' | 'DELETE' | 'ADMIN';
  granted_at: string;
}


