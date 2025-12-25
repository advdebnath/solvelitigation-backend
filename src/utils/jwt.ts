import * as jwt from "jsonwebtoken";
import type { SignOptions } from "jsonwebtoken";

export function signToken(
  payload: object,
  secret: string,
  expiresIn: SignOptions["expiresIn"] = "7d",
): string {
  return jwt.sign(payload, secret, { expiresIn });
}

export function verifyToken(token: string, secret: string): any {
  return jwt.verify(token, secret);
}
