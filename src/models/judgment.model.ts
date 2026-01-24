import mongoose, { Schema, Document } from "mongoose";

export interface IJudgment extends Document {
  courtType: "supreme" | "high" | "tribunal";
  pdfPath: string;
  originalName: string;
  fileName: string;
  fileSize: number;
  fileHash: string;
  uploadedBy?: string | null;
  uploadedAt: Date;
  nlpStatus: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
  nlpError?: string | null;
}

const JudgmentSchema = new Schema<IJudgment>(
  {
    courtType: {
      type: String,
      enum: ["supreme", "high", "tribunal"],
      required: true,
      index: true,
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

    /**
     * SHA-256 hash of PDF
     * Used to prevent duplicate uploads
     */
    fileHash: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },

    uploadedBy: {
      type: String,
      default: null,
      index: true,
    },

    uploadedAt: {
      type: Date,
      default: Date.now,
      index: true,
    },

    nlpStatus: {
      type: String,
      enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true,
    },

    nlpError: {
      type: String,
      default: null,
    },
  },
  {
    timestamps: false,
    versionKey: false,
  }
);

export const Judgment =
  mongoose.models.Judgment ||
  mongoose.model<IJudgment>("Judgment", JudgmentSchema);
