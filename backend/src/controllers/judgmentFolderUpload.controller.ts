import { Request, Response } from "express";
import crypto from "crypto";
import fs from "fs";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { uploadToGridFS } from "../utils/gridfs";

function extractDate(filename: string) {
  const patterns = [
    /\d{2}-[A-Za-z]{3}-\d{4}/,
    /\d{2}-\d{2}-\d{4}/,
    /\d{4}-\d{2}-\d{2}/
  ];

  for (const p of patterns) {
    const match = filename.match(p);
    if (match) {
      const d = new Date(match[0]);
      if (!isNaN(d.getTime())) return d;
    }
  }

  return new Date();
}

export const uploadJudgmentFolder = async (req: Request, res: Response) => {
  try {
    const files = req.files as Express.Multer.File[];
    const court = req.body.court;

    if (!court) {
      return res.status(400).json({ message: "Court selection required" });
    }

    if (!files || files.length === 0) {
      return res.status(400).json({ message: "No files uploaded" });
    }

    console.log("📁 Files received:", files.length);

    const ingestionDocs: any[] = [];
    let duplicateCount = 0;

    for (const file of files) {
      const filename = file.originalname;
      const detectedDate = extractDate(filename);

      const buffer = fs.readFileSync(file.path);
      const sha256 = crypto
        .createHash("sha256")
        .update(buffer)
        .digest("hex");

      // 🔥 DUPLICATE CHECK
      const existing = await JudgmentIngestion.findOne({
        "file.sha256": sha256
      });

      if (existing) {
        duplicateCount++;
        console.log("⚠ Duplicate skipped:", filename);
        fs.unlinkSync(file.path);
        continue;
      }

      const gridfsFileId = await uploadToGridFS(
        file.path,
        filename
      );

      try {
        fs.unlinkSync(file.path);
      } catch {
        console.warn("⚠ Could not delete temp file:", file.path);
      }

      ingestionDocs.push({
        source: "superadmin-dashboard",
        uploadType: "folder",
        extractedMeta: {
          year: detectedDate.getFullYear(),
          month: detectedDate.getMonth() + 1,
          date: detectedDate.getDate(),
        },
        file: {
          originalName: filename,
          relativePath:
            (file as any).webkitRelativePath || filename,
          size: file.size,
          sha256,
          gridfsFileId,
        },
        status: "QUEUED",
        queuedAt: new Date(),
        createdBy: req.user!._id,
      });
    }

    if (ingestionDocs.length > 0) {
      await JudgmentIngestion.insertMany(ingestionDocs);
    }

    return res.json({
      success: true,
      inserted: ingestionDocs.length,
      duplicatesSkipped: duplicateCount
    });

  } catch (err) {
    console.error("❌ Upload error:", err);
    return res.status(500).json({ message: "Upload failed" });
  }
};
