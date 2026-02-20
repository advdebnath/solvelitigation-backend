import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../../models/JudgmentIngestion";

export async function reprocessIngestion(req: Request, res: Response) {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid ingestion ID" });
    }

    const ingestion = await JudgmentIngestion.findById(id);

    if (!ingestion) {
      return res.status(404).json({ message: "Ingestion not found" });
    }

    if (ingestion.status !== "PERMANENT_FAILURE") {
      return res.status(400).json({
        message: "Only PERMANENT_FAILURE ingestions can be reprocessed",
      });
    }

    ingestion.status = "QUEUED";
    ingestion.retryCount = 0;
    ingestion.error = undefined;
    ingestion.permanentFailureAt = undefined;
    ingestion.queuedAt = new Date();

    await ingestion.save();

    return res.json({
      success: true,
      message: "Ingestion requeued successfully",
    });
  } catch (err) {
    console.error("Reprocess failed:", err);
    return res.status(500).json({ message: "Reprocess failed" });
  }
}
