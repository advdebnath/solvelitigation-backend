import mongoose from "mongoose";

export const saveFileToGridFS = async (
  fileStream: NodeJS.ReadableStream,
  filename: string
): Promise<mongoose.Types.ObjectId> => {
  const db = mongoose.connection.db;

  if (!db) {
    throw new Error("MongoDB connection not ready");
  }

  const bucket = new mongoose.mongo.GridFSBucket(db, {
    bucketName: "judgments",
  });

  return new Promise((resolve, reject) => {
    const uploadStream = bucket.openUploadStream(filename);

    fileStream
      .pipe(uploadStream)
      .on("error", reject)
      .on("finish", () =>
        resolve(uploadStream.id as mongoose.Types.ObjectId)
      );
  });
};
