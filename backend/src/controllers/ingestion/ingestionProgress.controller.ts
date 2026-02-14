import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

/**
 * GET /api/ingestions/progress
 * Returns aggregated ingestion progress
 */
export async function getIngestionProgress(
  req: Request,
  res: Response
) {
  try {
    const stats = await JudgmentIngestion.aggregate([
      {
        $group: {
          _id: "$status",
          count: { $sum: 1 },
        },
      },
    ]);

    // Normalize response
    const progress = {
      total: 0,
      uploaded: 0,
      queued: 0,
      processing: 0,
      completed: 0,
      failed: 0,
    };

    for (const s of stats) {
      progress.total += s.count;

      switch (s._id) {
        case "UPLOADED":
          progress.uploaded = s.count;
          break;
        case "QUEUED":
          progress.queued = s.count;
          break;
        case "PROCESSING":
          progress.processing = s.count;
          break;
        case "COMPLETED":
          progress.completed = s.count;
          break;
        case "FAILED":
          progress.failed = s.count;
          break;
      }
    }

    return res.json({
      success: true,
      progress,
    });
  } catch (error) {
    console.error("❌ Ingestion progress error:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch ingestion progress",
    });
  }
}
