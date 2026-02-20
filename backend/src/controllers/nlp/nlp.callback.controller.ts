import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../../models/JudgmentIngestion";

export const nlpCallbackController = async (req: Request, res: Response) => {
  try {
    const { ingestionId, status, error } = req.body;

    if (!mongoose.Types.ObjectId.isValid(ingestionId)) {
      return res.status(400).json({ message: "Invalid ingestionId" });
    }

    const ingestion = await JudgmentIngestion.findById(ingestionId);

    if (!ingestion) {
      return res.status(404).json({ message: "Ingestion not found" });
    }

    // 🔴 FAILURE WITH ESCALATION
    if (status === "FAILED") {
      ingestion.retryCount = (ingestion.retryCount || 0) + 1;

      if (ingestion.retryCount >= 3) {
        ingestion.status = "PERMANENT_FAILURE";
        ingestion.permanentFailureAt = new Date();
        console.log("🚨 Permanent failure:", ingestionId);
      } else {
        ingestion.status = "QUEUED"; // re-queue instead of RETRY
        console.log("🔁 Re-queued for retry:", ingestionId);
      }

      ingestion.error = error || "NLP processing failed";
      ingestion.failedAt = new Date();

      await ingestion.save();

      return res.json({
        success: true,
        ingestionId,
        retryCount: ingestion.retryCount,
        status: ingestion.status
      });
    }

    // 🟢 SUCCESS
    if (status === "COMPLETED") {
      ingestion.status = "COMPLETED";
      ingestion.completedAt = new Date();

      await ingestion.save();

      return res.json({
        success: true,
        ingestionId,
        status: ingestion.status
      });
    }

    return res.status(400).json({ message: "Invalid status" });

  } catch (err) {
    console.error("❌ NLP callback error:", err);
    return res.status(500).json({ message: "Callback failed" });
  }
};
