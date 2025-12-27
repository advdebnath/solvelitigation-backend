import jwt, { SignOptions } from "jsonwebtoken";
import cfg from "@/config";

export interface JwtPayload {
  userId: string;
  role: string;
}

export function signToken(
  payload: JwtPayload,
  secret: string = cfg.jwtSecret,
  expiresIn: SignOptions["expiresIn"] = "7d"
): string {
  const options: SignOptions = { expiresIn };
  return jwt.sign(payload, secret, options);
}

export function verifyToken(
  token: string,
  secret: string = cfg.jwtSecret
): JwtPayload {
  return jwt.verify(token, secret) as JwtPayload;
}
