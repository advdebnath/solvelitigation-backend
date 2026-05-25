import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

// ============================================
// 🔥 GET FAILED INGESTIONS
// ============================================

export const getFailedIngestions = async (
  _req: Request,
  res: Response
) => {
  try {
    const failed = await JudgmentIngestion.find({
      status: "FAILED",
    })
      .sort({ updatedAt: -1 })
      .limit(50);

    const count = await JudgmentIngestion.countDocuments({
      status: "FAILED",
    });

    res.json({
      success: true,
      count,
      data: failed,
    });

  } catch (err) {
    console.error("❌ Failed ingestion fetch error:", err);
    res.status(500).json({ success: false });
  }
};

// ============================================
// 🔥 RETRY FAILED INGESTION (FIXED)
// ============================================

export const retryFailedIngestion = async (
  req: Request,
  res: Response
) => {
  try {
    const { id } = req.params;

    const ingestion = await JudgmentIngestion.findById(id);

    if (!ingestion) {
      return res.status(404).json({ success: false });
    }

    if (ingestion.status !== "FAILED") {
      return res.status(400).json({
        success: false,
        message: "Only FAILED ingestions can be retried",
      });
    }

    // 🔥 CLEAN RESET (PERMANENT FIX)
    ingestion.status = "QUEUED";
    ingestion.progress = 0;
    ingestion.stage = "QUEUED";

    ingestion.error = undefined;
    ingestion.lastErrorAt = undefined;

    ingestion.retryCount = 0;
    ingestion.isLocked = false;

    ingestion.queuedAt = new Date();

    await ingestion.save();

    res.json({
      success: true,
      message: "Ingestion requeued successfully",
    });

  } catch (err) {
    console.error("❌ Retry error:", err);
    res.status(500).json({ success: false });
  }
};

// ============================================
// 🔥 GET INGESTION STATS (UPDATED)
// ============================================

export const getIngestionStats = async (
  _req: Request,
  res: Response
) => {
  try {
    const stats = await JudgmentIngestion.aggregate([
      {
        $group: {
          _id: "$status",
          count: { $sum: 1 },
        },
      },
    ]);

    // 🔥 UPDATED STATUS STRUCTURE
    const result: any = {
      UPLOADED: 0,
      QUEUED: 0,
      PROCESSING: 0,
      COMPLETED: 0,
      FAILED: 0,
      PERMANENT_FAILURE: 0,
      TOTAL: 0,
    };

    for (const item of stats) {
      if (result[item._id] !== undefined) {
        result[item._id] = item.count;
      }
      result.TOTAL += item.count;
    }

    res.json({
      success: true,
      data: result,
    });

  } catch (err) {
    console.error("❌ Ingestion stats error:", err);
    res.status(500).json({ success: false });
  }
};
