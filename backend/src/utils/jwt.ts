// src/utils/jwt.ts
import jwt, { JwtPayload, SignOptions } from "jsonwebtoken";

/**
 * IMPORTANT:
 * - dotenv MUST NOT be used here
 * - env vars are read lazily inside functions
 */

export interface AppJwtPayload {
  userId: string;
  role: string;
}

/**
 * Get secret lazily (runtime-safe)
 */
function getJwtSecret(): string {
  const secret = process.env.JWT_SECRET;
  if (!secret) {
    throw new Error("JWT_SECRET not defined");
  }
  return secret;
}

/**
 * Sign JWT
 */
export function signToken(
  payload: AppJwtPayload,
  expiresIn: SignOptions["expiresIn"] = "7d"
): string {
  return jwt.sign(payload, getJwtSecret(), { expiresIn });
}

/**
 * Verify JWT
 */
export function verifyToken<T extends JwtPayload = JwtPayload>(
  token: string
): T {
  return jwt.verify(token, getJwtSecret()) as T;
}
