import { Request, Response } from "express";
import crypto from "crypto";
import { Judgment } from "../../models/judgment.model";
import { enqueueNlpJob } from "../../utils/nlpEnqueue";

export const retryNlpJob = async (req: Request, res: Response) => {
  try {
    const { judgmentId } = req.params;

    // 🔒 Validate ObjectId early
    if (!judgmentId.match(/^[0-9a-fA-F]{24}$/)) {
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

    // 🔒 Only FAILED jobs are retryable
    if (judgment.nlp.status !== "FAILED") {
      return res.status(400).json({
        success: false,
        message: "Only FAILED NLP jobs can be retried",
      });
    }

    // 🔐 ALWAYS generate a NEW lockId
    const lockId = `NLP-${crypto.randomUUID()}`;

    // ♻ Reset NLP state
    judgment.nlp.status = "PENDING";
    judgment.nlp.lockId = lockId;
    judgment.nlp.retryCount = (judgment.nlp.retryCount || 0) + 1;
    judgment.nlp.lastError = undefined;
    judgment.nlp.startedAt = undefined;
    judgment.nlp.completedAt = undefined;

    await judgment.save();

    // 🚀 Enqueue NLP again
    await enqueueNlpJob({
      judgmentId: judgment._id.toString(),
      lockId,
      pdfPath: judgment.filePath,
    });

    return res.json({
      success: true,
      message: "NLP job retried",
      lockId,
      retryCount: judgment.nlp.retryCount,
    });
  } catch (error) {
    console.error("NLP RETRY ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to retry NLP job",
    });
  }
};
