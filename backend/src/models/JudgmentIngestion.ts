import mongoose, { Schema, Document } from "mongoose";

export type IngestionStatus =
  | "UPLOADED"
  | "QUEUED"
  | "PROCESSING"
  | "COMPLETED"
  | "FAILED";

export interface IJudgmentIngestion extends Document {
  source: string;
  uploadType: "single" | "folder";

  file: {
    originalName: string;
    relativePath: string;
    size: number;
    sha256: string;
    gridfsFileId: mongoose.Types.ObjectId;
  };

  extractedMeta?: {
    year?: number;
    month?: number;
    date?: number;
  };

  status: IngestionStatus;
  error?: string;
  retryCount: number;

  queuedAt?: Date;
  processingAt?: Date;
  completedAt?: Date;
  failedAt?: Date;

  judgmentId?: mongoose.Types.ObjectId;

  createdBy: mongoose.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const JudgmentIngestionSchema = new Schema<IJudgmentIngestion>(
  {
    source: {
      type: String,
      required: true,
      index: true,
    },

    uploadType: {
      type: String,
      enum: ["single", "folder"],
      required: true,
    },

    file: {
      originalName: { type: String },
      relativePath: { type: String },
      size: { type: Number },
      sha256: { type: String },
      gridfsFileId: {
        type: Schema.Types.ObjectId,
        required: true,
        index: true,
      },
    },

    extractedMeta: {
      year: Number,
      month: Number,
      date: Number,
    },

    status: {
      type: String,
      enum: ["UPLOADED", "QUEUED", "PROCESSING", "COMPLETED", "FAILED"],
      default: "UPLOADED",
      index: true,
    },

    error: {
      type: String,
    },

    retryCount: {
      type: Number,
      default: 0,
    },

    queuedAt: Date,
    processingAt: Date,
    completedAt: Date,
    failedAt: Date,

    judgmentId: {
      type: Schema.Types.ObjectId,
      ref: "Judgment",
      index: true,
    },

    createdBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<IJudgmentIngestion>(
  "JudgmentIngestion",
  JudgmentIngestionSchema
);
