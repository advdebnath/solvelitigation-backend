import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../../models/JudgmentIngestion";
import Judgment from "../../models/judgment.model";

/**
 * POST /api/nlp/callback
 * Called by NLP service after processing
 */
export async function nlpCallbackController(
  req: Request,
  res: Response
) {
  const session = await mongoose.startSession();
  session.startTransaction();

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

    const ingestion = await JudgmentIngestion
      .findById(ingestionId)
      .session(session);

    if (!ingestion) {
      return res.status(404).json({
        message: "Ingestion record not found",
      });
    }

    // 🔒 Idempotency
    if (ingestion.status === "COMPLETED") {
      await session.commitTransaction();
      session.endSession();
      return res.json({
        success: true,
        message: "Already processed",
        judgmentId: ingestion.judgmentId,
      });
    }

    // ❌ Failure case
    if (status === "FAILED") {
      ingestion.status = "FAILED";
      ingestion.error = error || "NLP failed";
      ingestion.failedAt = new Date();
      await ingestion.save({ session });

      await session.commitTransaction();
      session.endSession();

      return res.json({ success: true, status: "FAILED" });
    }

    // ✅ COMPLETED → CREATE JUDGMENT
    if (status === "COMPLETED") {
      const judgment = await Judgment.create(
        [
          {
            ingestionId: ingestion._id,
            summary,
            category,
            subCategory,
            pointsOfLaw: pointsOfLaw || [],
            confidence,
            createdBy: ingestion.createdBy,
          },
        ],
        { session }
      );

      ingestion.status = "COMPLETED";
      ingestion.judgmentId = judgment[0]._id;
      ingestion.completedAt = new Date();

      await ingestion.save({ session });

      await session.commitTransaction();
      session.endSession();

      return res.json({
        success: true,
        ingestionId,
        judgmentId: judgment[0]._id,
        status: "COMPLETED",
      });
    }

    // 🟡 Other states (PROCESSING, QUEUED)
    ingestion.status = status;
    await ingestion.save({ session });

    await session.commitTransaction();
    session.endSession();

    return res.json({ success: true, status });
  } catch (err) {
    await session.abortTransaction();
    session.endSession();

    console.error("❌ NLP callback failed:", err);
    return res.status(500).json({
      message: "NLP callback failed",
    });
  }
}
