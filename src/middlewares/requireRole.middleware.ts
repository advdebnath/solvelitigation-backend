import { Request, Response, NextFunction } from "express";

export function requireRole(allowedRoles: Array<"user" | "admin" | "superadmin">) {
  return (_req: Request, res: Response, next: NextFunction) => {
    const role = res.locals.role;

    if (!role || !allowedRoles.includes(role)) {
      return res.status(403).json({
        success: false,
        message: "Access denied",
      });
    }

    next();
  };
}
