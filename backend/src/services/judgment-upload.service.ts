import mongoose, { Types } from "mongoose";
import Judgment from "../models/judgment.model";

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

  const judgment = await Judgment.create({
    title: file.originalname,
    filePath: file.path,
    originalFileName: file.originalname,

    uploadedBy: meta.uploadedBy,
    source: meta.source ?? "upload",

    status: "UPLOADED",
  });

  return judgment._id;
}
