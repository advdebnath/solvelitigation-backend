import { Readable } from "stream";
import mongoose from "mongoose";

export async function uploadToGridFS(
  file: Express.Multer.File,
  metadata: Record<string, any>
) {
  const db = mongoose.connection.db;
  if (!db) throw new Error("MongoDB not connected");

  const bucket = new mongoose.mongo.GridFSBucket(db, {
    bucketName: "judgments",
  });

  return new Promise<{ fileId: mongoose.Types.ObjectId }>((resolve, reject) => {
    const uploadStream = bucket.openUploadStream(file.originalname, {
      contentType: file.mimetype,
      metadata,
    });

    Readable.from(file.buffer)
      .pipe(uploadStream)
      .on("error", reject)
      .on("finish", () => resolve({ fileId: uploadStream.id }));
  });
}
