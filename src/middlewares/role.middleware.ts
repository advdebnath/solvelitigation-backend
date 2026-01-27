import { Request, Response, NextFunction } from "express";

type Role = "user" | "admin" | "superadmin";

export const requireRole =
  (...roles: Role[]) =>
  (req: Request, res: Response, next: NextFunction) => {
    const user = req.user || req.currentUser;

    if (!user || !roles.includes(user.role)) {
      return res.status(403).json({
        success: false,
        message: "Insufficient role permissions",
      });
    }

    next();
  };
