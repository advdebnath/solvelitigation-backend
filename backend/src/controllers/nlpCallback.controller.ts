import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../models/JudgmentIngestion";

/**
 * NLP CALLBACK (Option A - Ingestion Based)
 * Called by NLP worker
 */
export const nlpCallback = async (req: Request, res: Response) => {
  try {
    const { ingestionId, status, error } = req.body;

    if (!mongoose.Types.ObjectId.isValid(ingestionId)) {
      return res.status(400).json({
        success: false,
        message: "Invalid ingestionId",
      });
    }

    const update: any = {
      status,
      updatedAt: new Date(),
    };

    if (error) {
      update.error = error;
    }

    await JudgmentIngestion.findByIdAndUpdate(
      ingestionId,
      { $set: update }
    );

    return res.json({
      success: true,
      ingestionId,
      status,
    });

  } catch (err: any) {
    return res.status(500).json({
      success: false,
      message: "NLP callback failed",
      error: err.message,
    });
  }
};
