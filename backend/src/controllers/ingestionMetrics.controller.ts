import { Request, Response } from "express";
import JudgmentIngestion from "../models/JudgmentIngestion";

export const getIngestionMetrics = async (req: Request, res: Response) => {
  try {
    const total = await JudgmentIngestion.countDocuments();
    const completed = await JudgmentIngestion.countDocuments({ status: "COMPLETED" });
    const failed = await JudgmentIngestion.countDocuments({ status: "FAILED" });
    const processing = await JudgmentIngestion.countDocuments({ status: "PROCESSING" });
    const queued = await JudgmentIngestion.countDocuments({ status: "QUEUED" });
    const retrying = await JudgmentIngestion.countDocuments({
      status: "FAILED",
      retryCount: { $gt: 0 }
    });

    const successRate = total > 0 ? ((completed / total) * 100).toFixed(2) : "0";

    res.json({
      total,
      completed,
      failed,
      processing,
      queued,
      retrying,
      successRate: `${successRate}%`
    });
  } catch (err: any) {
    res.status(500).json({
      message: "Failed to fetch ingestion metrics",
      error: err.message
    });
  }
};
