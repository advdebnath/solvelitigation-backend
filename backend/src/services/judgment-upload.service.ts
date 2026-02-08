import path from "path";
import fs from "fs";
import mongoose from "mongoose";
import { uploadToGridFS } from "../utils/gridfs";

/**
 * ✅ Upload a judgment PDF into GridFS
 * - Handles large files (900MB)
 * - Returns GridFS ObjectId
 */
export async function uploadJudgmentFile(params: {
  localFilePath: string;
  originalName: string;
  metadata?: Record<string, any>;
}): Promise<mongoose.Types.ObjectId> {
  const { localFilePath, originalName, metadata = {} } = params;

  if (!fs.existsSync(localFilePath)) {
    throw new Error(`File not found: ${localFilePath}`);
  }

  const fileExt = path.extname(originalName).toLowerCase();
  if (fileExt !== ".pdf") {
    throw new Error("Only PDF files are allowed");
  }

  // ✅ Upload via canonical GridFS helper
  const gridFsId = await uploadToGridFS(
    localFilePath,
    originalName,
    metadata
  );

  return gridFsId;
}
