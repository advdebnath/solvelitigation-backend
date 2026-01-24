import { Request, Response } from "express";
import fs from "fs";
import crypto from "crypto";

import { enqueueNlpJob } from "@/utils/nlpEnqueue";
import { Judgment } from "@/models/judgment.model";

/**
 * POST /api/superadmin/judgments/upload
 * Single source of truth for judgment uploads
 */
export const uploadJudgments = async (req: Request, res: Response) => {
  try {
    /* ===================== VALIDATION ===================== */

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

    /* ===================== FILE METADATA ===================== */

    const {
      filename: fileName,
      originalname: originalName,
      size: fileSize,
      path: pdfPath,
    } = req.file;

    const fileSizeMB = +(fileSize / (1024 * 1024)).toFixed(2);
    const uploadedBy = (req as any).user?.userId ?? null;

    /* ===================== SHA-256 HASH ===================== */

    const fileBuffer = fs.readFileSync(pdfPath);
    const fileHash = crypto
      .createHash("sha256")
      .update(fileBuffer)
      .digest("hex");

    /* ===================== DUPLICATE CHECK ===================== */

    const existing = await Judgment.findOne({ fileHash }).select("_id");

    if (existing) {
      // Remove duplicate file immediately
      fs.unlinkSync(pdfPath);

      return res.status(409).json({
        success: false,
        message: "Duplicate judgment detected. This file already exists.",
      });
    }

    /* ===================== SAVE JUDGMENT ===================== */

    const judgment = await Judgment.create({
      courtType,
      pdfPath,
      originalName,
      fileName,
      fileSize,
      fileHash,
      uploadedBy,
      uploadedAt: new Date(),
      nlpStatus: "PENDING",
    });

    /* ===================== NLP QUEUE ===================== */

    await enqueueNlpJob({
      judgmentId: judgment._id.toString(),
      pdfPath,
      options: {
        cleanup: true,
        headnotes: true,
        pointsOfLaw: true,
      },
    });

    /* ===================== RESPONSE ===================== */

    return res.status(201).json({
      success: true,
      message: `${courtType.toUpperCase()} Court judgment (${fileSizeMB} MB) uploaded successfully`,
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
    console.error("❌ Judgment upload failed:", error);

    return res.status(500).json({
      success: false,
      message: "Upload failed",
      error: (error as Error).message,
    });
  }
};
