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

    const successRate =
      formatted.total > 0
        ? ((formatted.COMPLETED / formatted.total) * 100).toFixed(2)
        : "0";

    const failureRate =
      formatted.total > 0
        ? ((formatted.FAILED / formatted.total) * 100).toFixed(2)
        : "0";

    const retrying = await JudgmentIngestion.countDocuments({
      retryCount: { $gt: 0 }
    });

    const last24h = await JudgmentIngestion.countDocuments({
      createdAt: {
        $gte: new Date(Date.now() - 24 * 60 * 60 * 1000)
      }
    });

    return res.json({
      success: true,
      data: {
        ...formatted,
        retrying,
        last24h,
        successRate: `${successRate}%`,
        failureRate: `${failureRate}%`
      }
    });

  } catch (error: any) {
    return res.status(500).json({
      success: false,
      message: "Failed to fetch ingestion stats",
      error: error.message
    });
  }
};
