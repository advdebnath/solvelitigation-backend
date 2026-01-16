import mongoose, { Schema, Document } from "mongoose";

export interface IJudgment extends Document {
  courtType: "supreme" | "high" | "tribunal";
  pdfPath: string;
  originalName: string;
  fileName: string;
  fileSize: number;
  uploadedBy?: string | null;
  uploadedAt: Date;
  nlpStatus: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
}

const JudgmentSchema = new Schema<IJudgment>({
  courtType: {
    type: String,
    enum: ["supreme", "high", "tribunal"],
    required: true,
  },
  pdfPath: {
    type: String,
    required: true,
  },
  originalName: {
    type: String,
    required: true,
  },
  fileName: {
    type: String,
    required: true,
  },
  fileSize: {
    type: Number,
    required: true,
  },
  uploadedBy: {
    type: String,
    default: null,
  },
  uploadedAt: {
    type: Date,
    default: Date.now,
  },
  nlpStatus: {
    type: String,
    enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
    default: "PENDING",
  },
});

export const Judgment =
  mongoose.models.Judgment ||
  mongoose.model<IJudgment>("Judgment", JudgmentSchema);
