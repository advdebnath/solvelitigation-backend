import fs from "fs";
import mongoose from "mongoose";
import { GridFSBucket } from "mongodb";

/**
 * ✅ Get GridFS bucket (native MongoDB, safe cast)
 */
export function getGridFSBucket(): GridFSBucket {
  const db = mongoose.connection.db;

  if (!db) {
    throw new Error("MongoDB not connected");
  }

  return new GridFSBucket(db as unknown as import("mongodb").Db, {
    bucketName: "judgment_pdfs",
  });
}

/**
 * ✅ Upload local file (disk → GridFS stream)
 * SAFE for large files (900MB+)
 */
export async function uploadToGridFS(
  localFilePath: string,
  originalName: string,
  metadata: Record<string, any> = {}
): Promise<mongoose.Types.ObjectId> {
  const bucket = getGridFSBucket();

  return new Promise((resolve, reject) => {
    const uploadStream = bucket.openUploadStream(originalName, {
      metadata,
    });

    fs.createReadStream(localFilePath)
      .pipe(uploadStream)
      .on("error", (err: Error) => {
        reject(err);
      })
      .on("finish", () => {
        resolve(new mongoose.Types.ObjectId(uploadStream.id.toString()));
      });
  });
}
