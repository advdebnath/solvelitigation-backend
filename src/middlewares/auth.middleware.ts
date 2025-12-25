import config from "../config";
import type { Request, Response, NextFunction } from "express";
import * as jwt from "jsonwebtoken";
import { verifyToken } from "../utils/jwt";
import type { Role, RequestWithUser } from "../types/custom";

const COOKIE_NAME: string = process.env.AUTH_COOKIE_NAME || "sl_auth";

const JWT_SECRET: string =
  config.jwtSecret ||
  config?.jwtSecret ||
  process.env.JWT_SECRET ||
  "supersecret";

/* -------------------------------------------------------------------------- */
/* 🔒 Primary Authentication Middleware (Bearer preferred, Cookie fallback)   */
/* -------------------------------------------------------------------------- */
export const authenticateJWT = (
  req: RequestWithUser,
  res: Response,
  next: NextFunction,
) => {
  try {
    let token: string | undefined;
    const authHeader = req.headers.authorization;

    if (authHeader?.startsWith("Bearer ")) token = authHeader.split(" ")[1];
    if (!token && req.cookies?.[COOKIE_NAME]) token = req.cookies[COOKIE_NAME];

    if (!token) {
      return res.status(401).json({ success: false, message: "Unauthorized" });
    }

    let payload: any;
    try {
      payload = verifyToken(token, JWT_SECRET) as any;
    } catch {
      payload = jwt.verify(token, JWT_SECRET) as any;
    }

    const userId = payload.sub || payload._id || payload.id;
    if (!userId) {
      return res
        .status(401)
        .json({ success: false, message: "Invalid token payload" });
    }

    req.user = {
      id: String(userId),
      email: payload.email ?? "",
      role: (payload.role as Role) ?? "user",
    };

    (req as any).auth = payload;
    next();
  } catch (err) {
    console.error("[auth.middleware] Invalid JWT:", err);
    return res
      .status(401)
      .json({ success: false, message: "Invalid or expired token" });
  }
};

export const optionalAuth = (
  req: RequestWithUser,
  _res: Response,
  next: NextFunction,
) => {
  let token: string | undefined;
  const authHeader = req.headers.authorization;

  if (authHeader?.startsWith("Bearer ")) token = authHeader.split(" ")[1];
  if (!token && req.cookies?.[COOKIE_NAME]) token = req.cookies[COOKIE_NAME];

  if (token) {
    try {
      let payload: any;
      try {
        payload = verifyToken(token, JWT_SECRET) as any;
      } catch {
        payload = jwt.verify(token, JWT_SECRET) as any;
      }

      const userId = payload.sub || payload._id || payload.id;
      if (userId) {
        req.user = {
          id: String(userId),
          email: payload.email ?? "",
          role: (payload.role as Role) ?? "user",
        };
        (req as any).auth = payload;
      }
    } catch {
      console.warn("[auth.middleware] Optional auth ignored");
    }
  }

  next();
};

export const authenticateJWTOptional = optionalAuth;

/* -------------------------------------------------------------------------- */
/* 🔐 Role-Based Access Control                                               */
/* -------------------------------------------------------------------------- */
export const requireRole = (role: Role) => {
  return (req: RequestWithUser, res: Response, next: NextFunction) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({
        success: false,
        message: `Forbidden: ${role} role required`,
      });
    }
    next();
  };
};

export const authorizeRoles = (...roles: Role[]) => {
  return (req: RequestWithUser, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res
        .status(401)
        .json({ success: false, message: "Unauthorized: No user found" });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: `Forbidden: requires one of the following roles: ${roles.join(
          ", ",
        )}`,
      });
    }

    next();
  };
};

export const requireAdmin = (
  req: RequestWithUser,
  res: Response,
  next: NextFunction,
) => {
  if (!req.user) {
    return res
      .status(401)
      .json({ success: false, message: "Unauthorized: missing user" });
  }

  if (req.user.role !== "admin" && req.user.role !== "superadmin") {
    return res.status(403).json({
      success: false,
      message: "Forbidden: Only Admins or Superadmin are authorized",
    });
  }

  next();
};

export const requireSuperAdmin = requireRole("superadmin");

export default {
  authenticateJWT,
  authenticateJWTOptional,
  optionalAuth,
  requireRole,
  authorizeRoles,
  requireAdmin,
  requireSuperAdmin,
};

// ✅ Allow only Admin or Superadmin to proceed
export function requireAdminOrSuperAdmin(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const user: any = (req as any).user;

  if (!user) {
    return res
      .status(401)
      .json({ success: false, message: "Not authenticated" });
  }

  if (user.role !== "superadmin" && user.role !== "admin") {
    return res
      .status(403)
      .json({ success: false, message: "Admin or Superadmin required" });
  }

  next();
}
