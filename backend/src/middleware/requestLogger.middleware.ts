import { Request, Response, NextFunction } from "express";
import logger from "../utils/logger";

export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on("finish", () => {
    const duration = Date.now() - start;

    logger.info("HTTP Request", {
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      responseTimeMs: duration,
      userId: (req as any).user?._id || null,
      ip: req.ip,
    });
  });

  next();
}
