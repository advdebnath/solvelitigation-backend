import { Request, Response } from "express";
import crypto from "crypto";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { extractDateFromPath } from "../utils/extractDateFromPath";
import { validateJudgmentPath } from "../utils/validateJudgmentPath";
import { enqueueNlpForIngestion } from "../services/ingestionAutoEnqueue.service";

/**
 * POST /api/ingestions/upload-folder
 * Folder-only ingestion endpoint
 */
export const uploadJudgmentFolder = async (
  req: Request,
  res: Response
) => {
  try {
    const user = req.currentUser || req.user;
    if (!user) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    const files = req.files as Express.Multer.File[] | undefined;
    if (!files || files.length === 0) {
      return res.status(400).json({
        message: "Folder upload required. No files received.",
      });
    }

    const isFolderUpload = files.some(
      (f) => Boolean((f as any).webkitRelativePath)
    );

    if (!isFolderUpload) {
      return res.status(400).json({
        message:
          "Single PDF upload is disabled. Please upload a YEAR/MONTH/DATE folder.",
      });
    }

    let inserted = 0;
    let rejected = 0;
    const errors: Array<{ file: string; error: string }> = [];

    for (const file of files) {
      try {
        const relativePath =
          (file as any).webkitRelativePath || file.originalname;

        validateJudgmentPath(relativePath);

        const extracted = extractDateFromPath(relativePath);
        if (!extracted) {
          throw new Error("Invalid YEAR/MONTH/DATE folder structure");
        }

        const { year, month, day } = extracted;

        const sha256 = crypto
          .createHash("sha256")
          .update(`${file.originalname}:${file.size}`)
          .digest("hex");

        const ingestion = await JudgmentIngestion.create({
          source: "superadmin-dashboard",
          uploadType: "folder",
          file: {
            originalName: file.originalname,
            relativePath,
            size: file.size,
            sha256,
          },
          extractedMeta: {
            year,
            month,
            date: day,
          },
          status: "UPLOADED",
          createdBy: user._id,
        });

        enqueueNlpForIngestion(ingestion._id.toString()).catch((err: unknown) => {
          console.error(
            `❌ Auto-enqueue failed for ingestion ${ingestion._id}`,
            err
          );
        });

        inserted++;
      } catch (err: unknown) {
        rejected++;
        errors.push({
          file: file.originalname,
          error:
            err instanceof Error
              ? err.message
              : "Invalid file structure",
        });
      }
    }

    return res.status(200).json({
      success: true,
      message: "Folder uploaded successfully. Judgments are being ingested.",
      summary: {
        total: files.length,
        inserted,
        rejected,
      },
      errors,
    });
  } catch (error) {
    console.error("❌ Folder ingestion failed:", error);
    return res.status(500).json({
      message: "Folder ingestion failed",
    });
  }
};
