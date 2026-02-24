import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

export const getFailedIngestions = async (
  req: Request,
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
    console.error("Failed ingestion fetch error:", err);
    res.status(500).json({ success: false });
  }
};

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

    ingestion.status = "PENDING";
    ingestion.retryCount = 0;
    ingestion.error = undefined;

    await ingestion.save();

    res.json({
      success: true,
      message: "Ingestion moved to PENDING",
    });

  } catch (err) {
    console.error("Retry error:", err);
    res.status(500).json({ success: false });
  }
};

export const getIngestionStats = async (
  req: Request,
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

    const result: any = {
      UPLOADED: 0,
      PENDING: 0,
      PROCESSING: 0,
      COMPLETED: 0,
      FAILED: 0,
      PERMANENT_FAILURE: 0,
      TOTAL: 0,
    };

    for (const item of stats) {
      result[item._id] = item.count;
      result.TOTAL += item.count;
    }

    res.json({
      success: true,
      data: result,
    });

  } catch (err) {
    console.error("Ingestion stats error:", err);
    res.status(500).json({ success: false });
  }
};
