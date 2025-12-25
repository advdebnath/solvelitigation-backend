import { Request } from 'express';

export type Role = 'user' | 'admin' | 'superadmin';

export interface RequestWithUser extends Request {
  user?: {
    id: string;
    role: Role;
    email?: string;
  };
}
