import fs from "fs";
import path from "path";
import mongoose from "mongoose";
import { getGridFSBucket } from "../utils/gridfs";
import { Judgment } from "../models/judgment.model";

export async function storeJudgmentToGridFS({
  filePath,
  originalName,
  court,
  year,
  userId,
}: {
  filePath: string;
  originalName: string;
  court: string;
  year: number;
  userId: string;
}) {
  const bucket = getGridFSBucket();

  const uploadStream = bucket.openUploadStream(originalName, {
    metadata: { court, year },
  });

  await new Promise<void>((resolve, reject) => {
    fs.createReadStream(filePath)
      .pipe(uploadStream)
      .on("error", reject)
      .on("finish", resolve);
  });

  const judgment = await Judgment.create({
    title: path.basename(originalName, ".pdf"),
    court,
    year,
    gridfsFileId: uploadStream.id,
    originalFileName: originalName,
    uploadedBy: new mongoose.Types.ObjectId(userId),
  });

  fs.unlinkSync(filePath); // 🔥 cleanup

  return judgment;
}
