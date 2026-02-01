import axios from "axios";
import { Request, Response } from "express";
import fs from "fs";

import { saveFileToGridFS } from "../utils/saveToGridFS";
import { Judgment } from "../models/judgment.model";

export const uploadSingleJudgment = async (
  req: Request,
  res: Response
) => {
  try {
    // 1️⃣ FILE CHECK
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No PDF file uploaded",
      });
    }

    // 2️⃣ REQUIRED INGESTION METADATA
    const { courtType, year, month, date } = req.body;

    if (!courtType || !year || !month || !date) {
      return res.status(400).json({
        success: false,
        message: "courtType, year, month, date are required",
      });
    }

    // 3️⃣ STREAM FILE FROM DISK
    const fileStream = fs.createReadStream(req.file.path);

    // 4️⃣ SAVE TO GRIDFS
    const gridfsFileId = await saveFileToGridFS(
      fileStream,
      req.file.originalname
    );

    // 5️⃣ AUTO-GENERATED TITLE (STABLE & DETERMINISTIC)
    const title = `${courtType} Judgment (${year}-${month}-${date})`;

    // 6️⃣ CREATE JUDGMENT RECORD (NLP-FIRST DESIGN)
    const judgment = await Judgment.create({
      title,
      year: Number(year),
      gridfsFileId,

      status: "UPLOADED",

      nlp: {
        status: "PENDING",
        pointsOfLaw: [],
        acts: [],
      },
    });

    // 7️⃣ ENQUEUE NLP PROCESS (NON-BLOCKING)
    try {
      await axios.post("http://127.0.0.1:8000/enqueue", {
        jobId: judgment._id.toString(),
        pdfPath: req.file.path,
      });
    } catch (nlpErr) {
      console.error("⚠️ NLP enqueue failed:", nlpErr);
      // Upload must NOT fail if NLP is down
    }

    // 8️⃣ RESPONSE
    return res.json({
      success: true,
      judgmentId: judgment._id,
      nlpStatus: judgment.nlp.status,
    });

  } catch (error) {
    console.error("UPLOAD ERROR:", error);

    const err = error as Error;
    return res.status(500).json({
      success: false,
      message: err.message || "Judgment upload failed",
      stack: process.env.NODE_ENV === "development" ? err.stack : undefined,
    });
  }
};
