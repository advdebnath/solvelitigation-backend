import dotenv from "dotenv";
import jwt, { JwtPayload as JwtLibPayload } from "jsonwebtoken";

/**
 * Load environment variables explicitly
 * (required for PM2 + compiled dist/)
 */
dotenv.config({
  path: process.env.NODE_ENV === "production"
    ? ".env.production"
    : ".env",
});

/**
 * Resolve and validate secret ONCE
 */
const RAW_JWT_SECRET = process.env.JWT_SECRET;

if (!RAW_JWT_SECRET) {
  throw new Error("JWT_SECRET not defined");
}

/**
 * After this point, TypeScript knows this is a string
 */
const JWT_SECRET: string = RAW_JWT_SECRET;

/**
 * App-level payload
 */
export interface AppJwtPayload {
  userId: string;
  role: string;
}

/**
 * Sign token
 */
export function signToken(payload: AppJwtPayload): string {
  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: "7d",
  });
}

/**
 * Verify token
 */
export function verifyToken(token: string): AppJwtPayload {
  const decoded = jwt.verify(token, JWT_SECRET) as JwtLibPayload;

  return {
    userId: decoded.userId as string,
    role: decoded.role as string,
  };
}
