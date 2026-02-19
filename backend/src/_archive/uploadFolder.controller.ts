import { Request, Response, NextFunction } from "express";
import path from "path";
import crypto from "crypto";
import fs from "fs";
import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueIngestions } from "../services/ingestion-enqueue.service";

export const uploadFolderController = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const files = req.files as Express.Multer.File[];

    if (!files || files.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No PDF files found in uploaded folder",
      });
    }

    const ingestions: any[] = [];

    for (const file of files) {
      if (!file.originalname.toLowerCase().endsWith(".pdf")) continue;

      const relativePath =
        (file as any).webkitRelativePath || file.originalname;

      const parts = relativePath.split("/");

      let year: number | undefined;
      let month: number | undefined;
      let date: number | undefined;

      if (parts.length >= 4) {
        year = Number(parts[0]) || undefined;
        month = Number(parts[1]) || undefined;
        date = Number(parts[2]) || undefined;
      }

      // ✅ Correct SHA256 using disk file
      const fileBuffer = fs.readFileSync(file.path);
      const sha256 = crypto
        .createHash("sha256")
        .update(fileBuffer)
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
          date,
        },

        status: "UPLOADED",
        createdBy: (req as any).user?._id,
      });

      ingestions.push(ingestion);
    }

    if (ingestions.length === 0) {
      return res.status(400).json({
        success: false,
        message: "Folder contained no valid PDF files",
      });
    }

    const ingestionIds = ingestions.map(i => i._id.toString());
    await enqueueIngestions(ingestionIds);

    return res.status(201).json({
      success: true,
      message: "Folder uploaded and queued successfully",
      count: ingestions.length,
    });
  } catch (err) {
    next(err);
  }
};
