import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import cfg from "@/config";

interface AuthPayload {
  userId: string;
  role: string;
}

export function authenticateJWT(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token = req.cookies?.sl_auth;

    if (!token) {
      return res.status(401).json({
        success: false,
        message: "Authentication required",
      });
    }

    const decoded = jwt.verify(token, cfg.jwtSecret) as AuthPayload;

    if (!decoded?.userId || !decoded?.role) {
      return res.status(401).json({
        success: false,
        message: "Invalid token payload",
      });
    }

    req.user = {
      userId: decoded.userId,
      role: decoded.role,
    };

    next();
  } catch {
    return res.status(401).json({
      success: false,
      message: "Invalid or expired token",
    });
  }
}

export function authenticateJWTOptional(
  req: Request,
  _res: Response,
  next: NextFunction
) {
  try {
    const token = req.cookies?.sl_auth;
    if (!token) return next();

    const decoded = jwt.verify(token, cfg.jwtSecret) as AuthPayload;
    if (decoded?.userId && decoded?.role) {
      req.user = {
        userId: decoded.userId,
        role: decoded.role,
      };
    }
  } catch {
    // ignore optional auth errors
  }
  next();
}
