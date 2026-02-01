import { Request, Response } from "express";
import { enqueueNlpJob } from "../../utils/nlpEnqueue";

export const enqueueNlpJobController = async (
  req: Request,
  res: Response
) => {
  try {
    const { judgmentId, lockId, pdfPath } = req.body;

    // 🔒 Strict validation
    if (!judgmentId || !lockId || !pdfPath) {
      return res.status(400).json({
        success: false,
        message: "judgmentId, lockId, and pdfPath are required",
      });
    }

    // 🧠 Enqueue NLP job
    await enqueueNlpJob({
      judgmentId,
      lockId,
      pdfPath,
    });

    return res.json({
      success: true,
      message: "NLP job enqueued",
    });
  } catch (error) {
    console.error("NLP ENQUEUE ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to enqueue NLP job",
    });
  }
};
