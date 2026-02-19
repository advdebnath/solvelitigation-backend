import { Request, Response } from "express";
import JudgmentIngestion from "../models/JudgmentIngestion";

export const getIngestionStats = async (req: Request, res: Response) => {
  try {
    const total = await JudgmentIngestion.countDocuments();

    const pending = await JudgmentIngestion.countDocuments({ status: "PENDING" });
    const processing = await JudgmentIngestion.countDocuments({ status: "PROCESSING" });
    const completed = await JudgmentIngestion.countDocuments({ status: "COMPLETED" });
    const failed = await JudgmentIngestion.countDocuments({ status: "FAILED" });

    const recent = await JudgmentIngestion.find()
      .sort({ createdAt: -1 })
      .limit(10)
      .select("_id status file.originalName createdAt");

    res.json({
      success: true,
      data: {
        total,
        pending,
        processing,
        completed,
        failed,
        recent,
      },
    });
  } catch (error) {
    console.error("Ingestion stats error:", error);
    res.status(500).json({ success: false, message: "Server error" });
  }
};
