import { Request, Response } from "express";
import crypto from "crypto";
import fs from "fs";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { uploadToGridFS } from "../utils/gridfs";

export const uploadJudgmentFolder = async (
  req: Request,
  res: Response
) => {
  try {
    console.log("🔥 NEW CONTROLLER LOADED");

    const files = req.files as Express.Multer.File[];
    console.log("DEBUG USER:", req.user);
    const court = req.body.court;

    if (!court) {
      return res.status(400).json({ message: "Court selection is required" });
    }

    if (!files || files.length === 0) {
      return res.status(400).json({ message: "No files uploaded" });
    }

    console.log("📁 Files received:", files.length);

    const ingestions = [];

    for (const file of files) {
      const filename = file.originalname;
      console.log("➡️ Processing file:", filename);

      const dateMatch = filename.match(/(\d{2})-(\d{2})-(\d{4})/);

      if (!dateMatch) {
        return res.status(400).json({
          message: `Date not found in filename: ${filename}`,
        });
      }

      const date = Number(dateMatch[1]);
      const month = Number(dateMatch[2]);
      const year = Number(dateMatch[3]);

      const buffer = fs.readFileSync(file.path);
      const sha256 = crypto
        .createHash("sha256")
        .update(buffer)
        .digest("hex");

      // await uploadToGridFS(file.path, file.originalname);

      const ingestion = new JudgmentIngestion({
        source: "superadmin-dashboard",
        uploadType: "folder",

        extractedMeta: {
          year,
          month,
          date,
        },

        file: {
          originalName: file.originalname,
          relativePath: file.originalname,  // ✅ FIXED
          size: file.size,
          sha256,
        },

        status: "QUEUED",
        queuedAt: new Date(),

        createdBy: req.user!._id,
      });

      await ingestion.save();
      console.log("INGESTION SAVED:", ingestion._id.toString());

      ingestions.push(ingestion);
    }

    return res.status(200).json({
      success: true,
      totalFiles: ingestions.length,
    });

  } catch (error) {
    console.error("❌ Upload failed:", error);
    return res.status(500).json({
      message: "Upload failed",
    });
  }
};
