import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../../models/JudgmentIngestion";
import { Judgment } from "../../models";

/**
 * POST /api/nlp/callback
 * Called by NLP service after processing
 */
export async function nlpCallbackController(
  req: Request,
  res: Response
) {
  try {
    const {
      ingestionId,
      status,
      summary,
      category,
      subCategory,
      pointsOfLaw,
      confidence,
      error,
    } = req.body;

    if (!ingestionId || !status) {
      return res.status(400).json({
        message: "ingestionId and status are required",
      });
    }

    if (!mongoose.Types.ObjectId.isValid(ingestionId)) {
      return res.status(400).json({
        message: "Invalid ingestionId",
      });
    }

    const ingestion = await JudgmentIngestion.findById(ingestionId);

    if (!ingestion) {
      return res.status(404).json({
        message: "Ingestion record not found",
      });
    }

    // 🔒 Idempotency: if already final
    if (["COMPLETED", "FAILED"].includes(ingestion.status)) {
      return res.json({
        success: true,
        message: "Callback already processed",
        ingestionId,
        status: ingestion.status,
      });
    }

    // ----------------------------
    // Handle FAILED
    // ----------------------------
    if (status === "FAILED") {
      ingestion.status = "FAILED";
      ingestion.error = error || "NLP processing failed";
      ingestion.failedAt = new Date();
      await ingestion.save();

      return res.json({
        success: true,
        ingestionId,
        status: "FAILED",
      });
    }

    // ----------------------------
    // Handle COMPLETED
    // ----------------------------
    if (status === "COMPLETED") {
      // 🔍 Check if judgment already exists
      const existingJudgment = await Judgment.findOne({
        ingestionId: ingestion._id,
      });

      if (existingJudgment) {
        ingestion.status = "COMPLETED";
        ingestion.completedAt = new Date();
        await ingestion.save();

        return res.json({
          success: true,
          message: "Judgment already created",
          judgmentId: existingJudgment._id,
        });
      }

      // 📝 Create Judgment
      const judgment = await Judgment.create({
        ingestionId: ingestion._id,
        summary,
        category,
        subCategory,
        pointsOfLaw,
        confidence,
        createdBy: ingestion.createdBy,
      });

      // 🔗 Update ingestion
      ingestion.status = "COMPLETED";
      ingestion.judgmentId = judgment._id;
      ingestion.completedAt = new Date();
      await ingestion.save();

      return res.json({
        success: true,
        ingestionId,
        judgmentId: judgment._id,
        status: "COMPLETED",
      });
    }

    // ----------------------------
    // Fallback
    // ----------------------------
    return res.status(400).json({
      message: "Unsupported status",
    });
  } catch (err) {
    console.error("❌ NLP callback failed:", err);
    return res.status(500).json({
      message: "NLP callback failed",
    });
  }
}
