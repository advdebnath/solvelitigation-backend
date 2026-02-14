export interface AuthUser {
  _id: string;      // MongoDB user id
  role: string;
  email?: string;
}
