import mongoose, { Types } from "mongoose";
import JudgmentIngestion from "../models/JudgmentIngestion";

/**
 * Creates a Judgment record from an uploaded PDF file
 * Used for both single and folder uploads
 */
export async function createJudgmentFromUpload(
  file: Express.Multer.File,
  meta: {
    uploadedBy: Types.ObjectId;
    source?: string;
  }
): Promise<Types.ObjectId | undefined> {
  // 🛡 Safety: multer already filtered PDFs
  if (!file || !file.originalname) {
    return undefined;
  }

  // 🧠 Extra safety (extension only, no mimetype)
  if (!file.originalname.toLowerCase().endsWith(".pdf")) {
    return undefined;
  }

  const ingestion = await JudgmentIngestion.create({
    filename: file.originalname,
    status: "UPLOADED",
    source: meta.source ?? "upload"
  });

  return ingestion._id;
}
