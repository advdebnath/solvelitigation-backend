import { Request, Response } from "express";
import path from "path";
import fs from "fs";
import crypto from "crypto";
import mongoose from "mongoose";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { uploadToGridFS } from "../utils/gridfs";

export const uploadFolderJudgments = async (req: Request, res: Response) => {
  try {
    /**
     * req.files populated by multer (folder upload)
     * req.body.pathMeta = { year, month, date }
     */
    const files = req.files as Express.Multer.File[];
    const { year, month, date } = req.body;

    if (!files?.length) {
      return res.status(400).json({ message: "No PDF files uploaded" });
    }

    if (!year || !month || !date) {
      return res.status(400).json({ message: "Missing pathMeta (year/month/date)" });
    }

    const ingestions = [];

    for (const file of files) {
      const buffer = fs.readFileSync(file.path);
      const sha256 = crypto.createHash("sha256").update(buffer).digest("hex");

      // Store PDF in GridFS



      const gridfsFileId = await uploadToGridFS(
  file.path,            // ✅ disk path from multer
  file.originalname,
  {
    size: file.size,
    mimetype: file.mimetype,
    uploadedBy: req.user?._id,
  }
);

      const ingestion = await JudgmentIngestion.create({
        source: "superadmin-dashboard",
        uploadType: "bulk",
        pathMeta: {
          year: Number(year),
          month: Number(month),
          date: Number(date),
        },
        file: {
          originalName: file.originalname,
          size: file.size,
          sha256,
          gridfsFileId,
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
    return res.status(500).json({ message: "Folder upload failed" });
  }
};
