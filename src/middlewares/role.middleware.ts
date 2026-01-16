import { Request, Response, NextFunction } from "express";

export function requireRole(roles: Array<"user" | "admin" | "superadmin">) {
  return (req: Request, res: Response, next: NextFunction) => {
    const role = res.locals.role;

    if (!role || !roles.includes(role)) {
      return res.status(403).json({
        success: false,
        message: "Access denied",
      });
    }

    next();
  };
}
