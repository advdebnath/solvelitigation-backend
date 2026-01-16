import { Request, Response } from "express";
import { NlpJob } from "@/models/nlpJob.model";
import { enqueueNlpJob } from "@/utils/nlpClient";

export const analyzeJudgment = async (req: Request, res: Response) => {
  const { judgmentId, pdfPath, options } = req.body;

  if (!judgmentId || !pdfPath) {
    return res.status(400).json({
      success: false,
      message: "judgmentId and pdfPath required",
    });
  }

  // -------------------------
  // Create NLP Job
  // -------------------------
  const job = await NlpJob.create({
    judgmentId,
    status: "QUEUED",
  });

  try {
    // -------------------------
    // Enqueue NLP Job
    // -------------------------
    await enqueueNlpJob({
      jobId: job._id.toString(),
      judgmentId,
      pdfPath,
      options,
    });
  } catch (err) {
    await NlpJob.findByIdAndUpdate(job._id, {
      status: "FAILED",
      error: "NLP service unreachable",
    });

    return res.status(503).json({
      success: false,
      message: "NLP service unavailable",
    });
  }

  return res.json({
    success: true,
    jobId: job._id,
    status: "QUEUED",
  });
};
