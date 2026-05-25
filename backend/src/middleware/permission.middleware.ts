import { Request, Response, NextFunction } from "express";

export const checkPermission = (allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = (req as any).user;

      if (!user || !user.role) {
        return res.status(401).json({ success: false, message: "Unauthorized" });
      }

      if (!allowedRoles.includes(user.role)) {
        return res.status(403).json({ success: false, message: "Forbidden" });
      }

      next();
    } catch (err) {
      return res
        .status(500)
        .json({ success: false, message: "Permission error" });
    }
  };
};
