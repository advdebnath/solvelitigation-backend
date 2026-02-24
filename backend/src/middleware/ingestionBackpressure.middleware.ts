import { Request, Response, NextFunction } from "express";
import JudgmentIngestion from "../models/JudgmentIngestion";
import logger from "../utils/logger";

export async function ingestionBackpressure(
  _req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const maxQueue = Number(process.env.INGESTION_MAX_QUEUE ?? 200);

    // 80% threshold
    const threshold = Math.floor(maxQueue * 0.8);

    const queuedCount = await JudgmentIngestion.countDocuments({
      status: "QUEUED",
    });

    if (queuedCount >= threshold) {
      logger.warn(
        `🚨 Backpressure activated | queued=${queuedCount} | threshold=${threshold}`
      );

      res.status(503).json({
        success: false,
        message:
          "System under high load. Please try again later.",
      });
      return;
    }

    next();
  } catch (error) {
    logger.error("❌ Backpressure middleware error:", error);

    res.status(500).json({
      success: false,
      message: "Backpressure validation failed.",
    });
  }
}
