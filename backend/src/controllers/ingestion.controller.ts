import { Request, Response } from "express";
import fs from "fs";
import crypto from "crypto";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { uploadToGridFS } from "../utils/gridfs";

export const uploadFolderJudgments = async (req: Request, res: Response) => {
  try {
    const files = req.files as Express.Multer.File[];
    const { year, month, date } = req.body;

    if (!files?.length) {
      return res.status(400).json({ message: "No PDF files uploaded" });
    }

    if (!year || !month || !date) {
      return res.status(400).json({
        message: "Missing year/month/date",
      });
    }

    const y = Number(year);
    const m = Number(month);
    const d = Number(date);

    if (
      y < 1950 ||
      m < 1 || m > 12 ||
      d < 1 || d > 31
    ) {
      return res.status(400).json({
        message: "Invalid year/month/date values",
      });
    }

    const ingestions = [];

    for (const file of files) {
      const buffer = fs.readFileSync(file.path);
      const sha256 = crypto
        .createHash("sha256")
        .update(buffer)
        .digest("hex");

      // ✅ Upload to GridFS (2 arguments only)
      await uploadToGridFS(file.path, file.originalname);

      const ingestion = await JudgmentIngestion.create({
        source: "superadmin-dashboard",
        uploadType: "folder",
        pathMeta: {
          year: y,
          month: m,
          date: d,
        },
        file: {
          originalName: file.originalname,
          size: file.size,
          sha256,
        },
        status: "UPLOADED",
        createdBy: req.user!._id,
      });

      ingestions.push(ingestion);
    }

    return res.json({
      success: true,
      count: ingestions.length,
      ingestionIds: ingestions.map(i => i._id),
    });

  } catch (err) {
    console.error("❌ Folder upload failed", err);
    return res.status(500).json({
      message: "Folder upload failed",
    });
  }
};
