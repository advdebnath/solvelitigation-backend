import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

export const getIngestionStats = async (_req: Request, res: Response) => {
  try {
    const stats = await JudgmentIngestion.aggregate([
      {
        $group: {
          _id: "$status",
          count: { $sum: 1 }
        }
      }
    ]);

    const formatted: any = {
      total: 0,
      UPLOADED: 0,
      QUEUED: 0,
      PROCESSING: 0,
      COMPLETED: 0,
      FAILED: 0
    };

    stats.forEach((s: any) => {
      formatted[s._id] = s.count;
      formatted.total += s.count;
    });

    return res.json({
      success: true,
      data: formatted
    });

  } catch (error: any) {
    return res.status(500).json({
      success: false,
      message: "Failed to fetch ingestion stats",
      error: error.message
    });
  }
};
