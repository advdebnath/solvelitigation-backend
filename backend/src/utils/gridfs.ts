import mongoose from "mongoose";
import fs from "fs";

export function getGridFSBucket() {
  if (!mongoose.connection.db) {
    throw new Error("MongoDB not connected");
  }

  return new mongoose.mongo.GridFSBucket(mongoose.connection.db, {
    bucketName: "judgments",
  });
}

export async function uploadToGridFS(
  filePath: string,
  filename: string
): Promise<mongoose.Types.ObjectId> {
  const bucket = getGridFSBucket();

  return new Promise((resolve, reject) => {
    const uploadStream = bucket.openUploadStream(filename);

    fs.createReadStream(filePath)
      .pipe(uploadStream)
      .on("error", reject)
      .on("finish", () => {
        resolve(uploadStream.id as mongoose.Types.ObjectId);
      });
  });
}
