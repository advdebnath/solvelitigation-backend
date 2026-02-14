import fs from "fs";
import path from "path";
import { getGridFSBucket } from "./gridfs";

export async function saveToGridFS(filePath: string, filename: string) {
  const bucket = getGridFSBucket();

  return new Promise((resolve, reject) => {
    const uploadStream = bucket.openUploadStream(filename);

    fs.createReadStream(filePath)
      .pipe(uploadStream)
      .on("error", reject)
      .on("finish", resolve);
  });
}
