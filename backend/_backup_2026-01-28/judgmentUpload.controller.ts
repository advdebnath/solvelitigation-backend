import axios from "axios";
import { Request, Response } from "express";
import fs from "fs";

import { saveFileToGridFS } from "../utils/saveToGridFS";
import { Judgment } from "../models/judgment.model";

export const uploadSingleJudgment = async (req: Request, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No PDF file uploaded",
      });
    }

    const { courtType, category, year } = req.body;

    if (!courtType || !category || !year) {
      return res.status(400).json({
        success: false,
        message: "courtType, category, year are required",
      });
    }

    // ✅ STREAM FROM DISK (correct for multer.diskStorage)
    const fileStream = fs.createReadStream(req.file.path);

    // ✅ SAVE TO GRIDFS
    const gridFsId = await saveFileToGridFS(
      fileStream,
      req.file.originalname
    );

    // ✅ CREATE JUDGMENT RECORD
    const judgment = await Judgment.create({
      courtType,
      category,
      year: Number(year),
      fileGridFsId: gridFsId,
      originalFileName: req.file.originalname,
      uploadedBy: req.currentUser!._id,
      status: "UPLOADED",
    });

    // 🔹 Enqueue NLP processing
     
      judgment.nlp = {
  status: "PROCESSING",
  pointsOfLaw: [],
  acts: [],
};

    await judgment.save();

    await axios.post("http://127.0.0.1:8000/enqueue", {
      jobId: judgment._id.toString(),
      pdfPath: req.file?.path,
    });

    return res.json({
      success: true,
      judgmentId: judgment._id,
status: judgment.status ?? "UPLOADED",      
    });
  } catch (error) {
    console.error("UPLOAD ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Judgment upload failed",
    });
  }
};
