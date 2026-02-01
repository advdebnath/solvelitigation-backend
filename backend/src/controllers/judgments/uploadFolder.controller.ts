import crypto from "crypto";
import fs from "fs";
import path from "path";
import { Request, Response } from "express";
import { Judgment } from "../../models/judgment.model";
import { enqueueNlpJob } from "../../utils/nlpEnqueue";

export const uploadJudgmentFolder = async (
  req: Request,
  res: Response
) => {
  try {
    const { uploadPath, courtType } = req.body;

    if (!uploadPath || !courtType) {
      return res.status(400).json({
        success: false,
        message: "uploadPath and courtType are required",
      });
    }

    if (!fs.existsSync(uploadPath)) {
      return res.status(400).json({
        success: false,
        message: "Upload path does not exist on server",
      });
    }

    const files = fs.readdirSync(uploadPath);
    const pdfFiles = files.filter((f) =>
      f.toLowerCase().endsWith(".pdf")
    );

    if (pdfFiles.length === 0) {
      return res.status(400).json({
        success: false,
        message: "No PDF files found in folder",
      });
    }

    let queued = 0;

    for (const file of pdfFiles) {
      // 🔑 UNIQUE lockId PER judgment (CRITICAL)
      const lockId = `NLP-${crypto.randomUUID()}`;

      const match = file.match(/(\d{4})(\d{2})(\d{2})/);
      if (!match) {
        console.warn(`Skipping file (date not found): ${file}`);
        continue;
      }

      const year = Number(match[1]);
      const month = Number(match[2]);
      const date = Number(match[3]);

      const fullPath = path.join(uploadPath, file);

      // 1️⃣ Create Judgment FIRST (store lockId)
      const judgment = await Judgment.create({
        courtType,
        category: "UNCLASSIFIED",
        year,
        month,
        date,
        originalFileName: file,
        filePath: fullPath,
        uploadedBy: req.currentUser?._id,
        status: "UPLOADED",
        nlp: {
          status: "PENDING",
          lockId,
          retryCount: 0,
        },
      });

      // 2️⃣ Enqueue NLP using SAME lockId
      await enqueueNlpJob({
        lockId,
        judgmentId: judgment._id.toString(),
        pdfPath: fullPath,
      });

      queued++;
    }

    return res.json({
      success: true,
      message: "Folder upload started",
      filesQueued: queued,
    });
  } catch (error) {
    console.error("UPLOAD FOLDER ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Folder upload failed",
    });
  }
};
