import { Request, Response } from "express";
import { Readable } from "stream";
import { getGridFSBucket } from "../../utils/gridfs";

export async function uploadJudgment(req: Request, res: Response) {
  if (!req.file) {
    return res.status(400).json({ message: "No file provided" });
  }

  const { courtType } = req.body;
  if (!courtType) {
    return res.status(400).json({ message: "courtType is required" });
  }

  const file = req.file; // ✔ type narrowed once

  const bucket = getGridFSBucket();

  const readable = new Readable();
  readable.push(file.buffer);
  readable.push(null);

  const uploadStream = bucket.openUploadStream(file.originalname, {
    metadata: {
      courtType,
      uploadedBy: req.currentUser?._id, // ✔ correct field
      uploadedAt: new Date(),
    },
  });

  readable.pipe(uploadStream);

  uploadStream.on("finish", () => {
    res.json({
      success: true,
      message: "Judgment uploaded to GridFS",
      fileId: uploadStream.id,
      filename: file.originalname,
      courtType,
    });
  });

  uploadStream.on("error", (err) => {
    console.error("GridFS upload error:", err);
    res.status(500).json({ message: "Upload failed" });
  });
}
