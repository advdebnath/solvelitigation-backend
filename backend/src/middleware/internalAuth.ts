import { Request, Response, NextFunction } from "express";

export const internalAuth = (req: Request, res: Response, next: NextFunction) => {
  const key = req.headers["x-internal-key"];

  if (key !== process.env.INTERNAL_API_KEY) {
    return res.status(401).json({
      success: false,
      message: "Unauthorized (internal)",
    });
  }

  next();
};
