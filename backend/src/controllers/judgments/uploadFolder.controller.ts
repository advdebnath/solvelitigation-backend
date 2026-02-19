import { Request, Response } from "express";
import path from "path";
import fs from "fs";
import mongoose from "mongoose";
import Judgment from "../../models/judgment.model";

function extractDateFromFilename(filename: string): Date | null {
  const patterns = [
    /\b(\d{2})[-_](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-_](\d{4})\b/i,
    /\b(\d{4})[-_](\d{2})[-_](\d{2})\b/,
    /\b(\d{2})[-_](\d{2})[-_](\d{4})\b/
  ];

  for (const pattern of patterns) {
    const match = filename.match(pattern);
    if (match) {
      const parsed = new Date(match[0]);
      if (!isNaN(parsed.getTime())) return parsed;
    }
  }

  return null;
}

export const uploadFolder = async (req: Request, res: Response) => {
  try {
    console.log("📥 Upload folder request received");

    const court = req.body?.court || "unknown";

    let files: Express.Multer.File[] = [];

    if (Array.isArray(req.files)) {
      files = req.files;
    } else if (req.files && typeof req.files === "object") {
      files = Object.values(req.files).flat() as Express.Multer.File[];
    }

    console.log("📁 Files count:", files.length);
    console.log("🏛 Court:", court);

    if (!files || files.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No files uploaded."
      });
    }

    const uploadedResults: any[] = [];

    for (const file of files) {
      const detectedDate = extractDateFromFilename(file.originalname);
      const finalDate = detectedDate || new Date();

      const year = finalDate.getFullYear().toString();
      const month = String(finalDate.getMonth() + 1).padStart(2, "0");
      const day = String(finalDate.getDate()).padStart(2, "0");

      const storageDir = path.join(
        process.cwd(),
        "uploads",
        "judgments",
        court,
        year,
        month,
        day
      );

      if (!fs.existsSync(storageDir)) {
        fs.mkdirSync(storageDir, { recursive: true });
      }

      const storagePath = path.join(storageDir, file.originalname);

      fs.renameSync(file.path, storagePath);

      const newJudgment = await Judgment.create({
        _id: new mongoose.Types.ObjectId(),
        fileName: file.originalname,
        filePath: storagePath,
        court,
        year,
        month,
        day,
        nlpStatus: "PENDING",
        uploadedAt: new Date()
      });

      uploadedResults.push({
        id: newJudgment._id,
        fileName: file.originalname,
        year,
        month,
        day
      });
    }

    return res.status(200).json({
      success: true,
      message: "Upload successful",
      totalFiles: uploadedResults.length,
      data: uploadedResults
    });

  } catch (error: any) {
    console.error("❌ Upload Folder Error:", error);

    return res.status(500).json({
      success: false,
      message: "Internal server error during folder upload."
    });
  }
};
