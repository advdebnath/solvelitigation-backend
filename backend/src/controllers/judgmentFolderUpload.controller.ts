import { Request, Response } from "express";
import crypto from "crypto";
import fs from "fs";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { uploadToGridFS } from "../utils/gridfs";

/**
 * Extract date from filename
 */
function extractDate(filename: string) {
  const patterns = [
    /\d{2}-[A-Za-z]{3}-\d{4}/, // 02-Feb-2021
    /\d{2}-\d{2}-\d{4}/,       // 02-02-2021
    /\d{4}-\d{2}-\d{2}/        // 2021-02-02
  ];

  for (const p of patterns) {
    const match = filename.match(p);
    if (match) {
      const d = new Date(match[0]);
      if (!isNaN(d.getTime())) return d;
    }
  }

  return new Date(); // fallback
}

export const uploadJudgmentFolder = async (req: Request, res: Response) => {
  try {
    console.log("🔥 NEW CONTROLLER LOADED");

    const files = req.files as Express.Multer.File[];
    const court = req.body.court;

    if (!court) {
      return res.status(400).json({ message: "Court selection required" });
    }

    if (!files || files.length === 0) {
      return res.status(400).json({ message: "No files uploaded" });
    }

    console.log("📁 Files received:", files.length);

    const ingestions: any[] = [];

    for (const file of files) {
      const filename = file.originalname;
      console.log("➡️ Processing:", filename);

      const detectedDate = extractDate(filename);

      // ✅ Read file for checksum
      const buffer = fs.readFileSync(file.path);
      const sha256 = crypto
        .createHash("sha256")
        .update(buffer)
        .digest("hex");

      // ✅ Upload to GridFS
      const gridfsFileId = await uploadToGridFS(
        file.path,
        filename
      );

      // ✅ Remove temp file after upload
      try {
        fs.unlinkSync(file.path);
      } catch (err) {
        console.warn("⚠ Could not delete temp file:", file.path);
      }

      // ✅ Create ingestion record
      const ingestion = new JudgmentIngestion({
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

      await ingestion.save();
      ingestions.push(ingestion);
    }

    return res.json({
      success: true,
      totalFiles: ingestions.length,
    });

  } catch (err) {
    console.error("❌ Upload error:", err);
    return res.status(500).json({ message: "Upload failed" });
  }
};
