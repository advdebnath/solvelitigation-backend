import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

/**
 * 🔁 POST /api/admin/retry-failed
 * Move all FAILED ingestions back to QUEUED
 */
export const retryFailedIngestions = async (
  req: Request,
  res: Response
) => {
  try {
    const result = await JudgmentIngestion.updateMany(
      {
        status: "FAILED",
        permanentFailureAt: { $exists: false }, // do not retry permanent failures
      },
      {
        $set: {
          status: "QUEUED",
        },
      }
    );

    return res.status(200).json({
      success: true,
      message: "Failed ingestions moved to QUEUED",
      retriedCount: result.modifiedCount,
    });
  } catch (error) {
    console.error("Retry failed error:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to retry ingestions",
    });
  }
};
