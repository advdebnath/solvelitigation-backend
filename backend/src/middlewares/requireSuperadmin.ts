import { Request, Response, NextFunction } from "express";

export function requireSuperadmin(
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (res.locals.role !== "superadmin") {
    return res.status(403).json({
      success: false,
      message: "Superadmin access required",
    });
  }

  next();
}
