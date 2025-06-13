export interface User {
  id: number;
  name: string;
  email: string;
  role: 'ADMIN' | 'USER';
  status: 'ACTIF' | 'INACTIF';
  createdAt?: Date;
  updatedAt?: Date;
} 