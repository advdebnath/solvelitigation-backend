import mongoose from "mongoose";
import { GridFSBucket } from "mongodb";

let bucket: GridFSBucket | null = null;

export function getGridFSBucket(): GridFSBucket {
  if (!mongoose.connection.db) {
    throw new Error("MongoDB not connected");
  }

  if (!bucket) {
    bucket = new GridFSBucket(
      mongoose.connection.db as any, // ✔ required for mongoose v8
      { bucketName: "judgments" }
    );
  }

  return bucket;
}
