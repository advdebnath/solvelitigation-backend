import { Request, Response } from "express";
import mongoose from "mongoose";
import axios from "axios";
import { Judgment } from "../../models";

/**
 * POST /api/nlp/retry/:judgmentId
 * Retry NLP processing for a judgment
 */
export const retryNlpJob = async (req: Request, res: Response) => {
  try {
    const { judgmentId } = req.params;

    if (!mongoose.Types.ObjectId.isValid(judgmentId)) {
      return res.status(400).json({
        success: false,
        message: "Invalid judgmentId",
      });
    }

    const judgment = await Judgment.findById(judgmentId);
    if (!judgment) {
      return res.status(404).json({
        success: false,
        message: "Judgment not found",
      });
    }

    // Allow retry only if NLP failed
    if (judgment.nlpStatus !== "FAILED") {
      return res.status(400).json({
        success: false,
        message: "Only FAILED NLP jobs can be retried",
      });
    }

    // ♻ Reset NLP state
    judgment.nlpStatus = "PENDING";
    await judgment.save();

    // 🚀 Re-enqueue NLP
    await axios.post("http://127.0.0.1:4000/api/nlp/enqueue", {
      judgmentId: judgment._id.toString(),
    });

    return res.json({
      success: true,
      message: "NLP retry queued",
      judgmentId,
      nlpStatus: "PENDING",
    });
  } catch (error) {
    console.error("NLP RETRY ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to retry NLP job",
    });
  }
};

export default retryNlpJob;
