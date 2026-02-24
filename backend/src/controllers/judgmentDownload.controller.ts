import { Request, Response } from "express";
import mongoose from "mongoose";
import Judgment from "../models/judgment.model";

export const downloadJudgmentPdf = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const judgment = await Judgment.findById(id);

    if (!judgment || !judgment.gridfsFileId) {
      return res.status(404).json({ message: "File not found" });
    }

    const bucket = new mongoose.mongo.GridFSBucket(
      mongoose.connection.db!,
      { bucketName: "judgments" }
    );

    res.set("Content-Type", "application/pdf");
    res.set(
      "Content-Disposition",
      `attachment; filename="judgment-${id}.pdf"`
    );

    const downloadStream = bucket.openDownloadStream(
      new mongoose.Types.ObjectId(judgment.gridfsFileId)
    );

    downloadStream.pipe(res);
  } catch (err) {
    console.error("Download error:", err);
    res.status(500).json({ message: "Download failed" });
  }
};
