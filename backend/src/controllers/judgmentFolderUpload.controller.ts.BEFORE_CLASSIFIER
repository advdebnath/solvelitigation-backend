import { Request, Response } from "express";
import crypto from "crypto";
import fs from "fs";
import path from "path";
import JudgmentIngestion from "../models/JudgmentIngestion";

/**
 * 🔹 Extract date from filename
 */
function extractDate(filename: string): Date {
  const patterns = [
    /\d{2}-[A-Za-z]{3}-\d{4}/,
    /\d{2}-\d{2}-\d{4}/,
    /\d{4}-\d{2}-\d{2}/
  ];

  for (const pattern of patterns) {
    const match = filename.match(pattern);
    if (match) {
      const parsed = new Date(match[0]);
      if (!isNaN(parsed.getTime())) return parsed;
    }
  }

  return new Date();
}

/**
 * 🔥 Detect Document Type
 */
function detectDocumentType(filename: string): string {
  const name = filename.toLowerCase();

  if (name.includes("rule")) return "RULE";
  if (name.includes("notification")) return "NOTIFICATION";
  if (name.includes("circular")) return "CIRCULAR";
  if (name.includes("act")) return "ACT";

  return "JUDGMENT";
}

/**
 * 🔥 Generate SAFE filename (PERMANENT FIX)
 */
function generateSafeFileName(file: Express.Multer.File): string {
  const raw =
    file.originalname ||
    file.filename ||
    path.basename(file.path) ||
    `Uploaded_File_${Date.now()}`;

  return raw
    .replace(/\s+/g, " ")
    .replace(/[^\w.\-]/g, "") // remove special chars
    .trim();
}

/**
 * 🔥 Upload Folder Controller (FINAL PRODUCTION VERSION)
 */
export const uploadJudgmentFolder = async (req: Request, res: Response) => {
  try {
    const files = req.files as Express.Multer.File[];
    const court = (req.body.court || "SUPREME").toUpperCase();

    if (!files || !Array.isArray(files) || files.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No files uploaded"
      });
    }

    console.log("📁 Files received:", files.length);

    const ingestionDocs: any[] = [];
    let duplicateCount = 0;

    for (const file of files) {
      // ============================================
      // 🔥 SAFE FILENAME (PERMANENT FIX)
      // ============================================
      const filename = generateSafeFileName(file);

      const detectedDate = extractDate(filename);
      const documentType = detectDocumentType(filename);

      console.log(`📌 Processing: ${filename} → ${documentType}`);

      // ============================================
      // 🔐 FILE EXISTENCE CHECK
      // ============================================
      if (!fs.existsSync(file.path)) {
        console.warn("⚠ File missing:", file.path);
        continue;
      }

      // ============================================
      // 🔐 SHA256 HASH
      // ============================================
      let sha256 = "";
      try {
        const buffer = fs.readFileSync(file.path);
        sha256 = crypto.createHash("sha256").update(buffer).digest("hex");
      } catch (err) {
        console.warn("⚠ SHA256 failed:", filename);
        continue;
      }

      // ============================================
      // 🔍 DUPLICATE CHECK
      // ============================================
      const existing = await JudgmentIngestion.findOne({
        "file.sha256": sha256
      }).lean();

      if (existing) {
        duplicateCount++;
        console.log("⚠ Duplicate skipped:", filename);
        continue;
      }

      // ============================================
      // ✅ FINAL DOCUMENT
      // ============================================
      ingestionDocs.push({
        source: "superadmin-dashboard",
        uploadType: "folder",
        courtType: court,

        fileName: filename, // 🔥 GUARANTEED SAFE

        documentType,

        extractedMeta: {
          year: detectedDate.getFullYear(),
          month: detectedDate.getMonth() + 1,
          date: detectedDate.getDate(),
        },

        file: {
          originalName: file.originalname || filename,
          relativePath: `uploads/judgments/${file.filename}`,
          size: file.size,
          sha256,
        },

        status: "QUEUED",
        stage: "QUEUED",
        progress: 0,
        isLocked: false,
        nlpQueued: false,
        retryCount: 0,
        maxRetries: 3,

        queuedAt: new Date(),
        createdBy: (req as any).user?._id || null,
      });
    }

    console.log("📦 Docs prepared:", ingestionDocs.length);

    if (ingestionDocs.length === 0) {
      return res.json({
        success: false,
        inserted: 0,
        duplicatesSkipped: duplicateCount,
      });
    }

    const inserted = await JudgmentIngestion.insertMany(ingestionDocs);

    console.log("✅ Inserted:", inserted.length);

    return res.json({
      success: true,
      inserted: inserted.length,
      duplicatesSkipped: duplicateCount,
    });

  } catch (err) {
    console.error("❌ Upload error:", err);
    return res.status(500).json({
      success: false,
      message: "Upload failed"
    });
  }
};
