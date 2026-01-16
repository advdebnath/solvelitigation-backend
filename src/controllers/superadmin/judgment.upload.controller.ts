import { Request, Response } from "express";
import { enqueueNlpJob } from "@/utils/nlpEnqueue";
import { Judgment } from "@/models/judgment.model";

export const uploadJudgments = async (req: Request, res: Response) => {
  try {
    // -------------------------
    // Validate upload
    // -------------------------
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No file uploaded",
      });
    }

    const { courtType } = req.body;

    if (!courtType || !["supreme", "high", "tribunal"].includes(courtType)) {
      return res.status(400).json({
        success: false,
        message: "Invalid court type. Must be: supreme, high, or tribunal",
      });
    }

    // -------------------------
    // File metadata
    // -------------------------
    const fileName = req.file.filename;
    const originalName = req.file.originalname;
    const fileSize = req.file.size;
    const fileSizeMB = (fileSize / (1024 * 1024)).toFixed(2);
    const pdfPath = req.file.path;

    const uploadedBy = (req as any).user?.userId || null;

    // -------------------------
    // PERMANENT: Save Judgment
    // -------------------------
    const judgment = await Judgment.create({
      courtType,
      pdfPath,
      originalName,
      fileName,
      fileSize,
      uploadedBy,
      uploadedAt: new Date(),
      nlpStatus: "PENDING",
    });

    // -------------------------
    // PERMANENT NLP ENQUEUE
    // -------------------------
    await enqueueNlpJob({
      judgmentId: judgment._id.toString(),
      pdfPath: judgment.pdfPath,
      options: {
        cleanup: true,
        headnotes: true,
        pointsOfLaw: true,
      },
    });

    // -------------------------
    // Response
    // -------------------------
    return res.json({
      success: true,
      message: `${
        courtType.charAt(0).toUpperCase() + courtType.slice(1)
      } Court judgment (${fileSizeMB}MB) uploaded successfully`,
      data: {
        judgmentId: judgment._id,
        fileName,
        originalName,
        fileSize,
        fileSizeMB,
        courtType,
        uploadedAt: judgment.uploadedAt,
      },
    });
  } catch (error) {
    console.error("❌ Upload error:", error);

    return res.status(500).json({
      success: false,
      message: "Upload failed",
      error: (error as Error).message,
    });
  }
};
