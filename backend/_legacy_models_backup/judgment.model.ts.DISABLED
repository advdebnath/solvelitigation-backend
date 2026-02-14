import mongoose, { Schema, Document } from "mongoose";

/**
 * TypeScript-only NLP status type
 */
export type NLPStatus =
  | "PENDING"
  | "RUNNING"
  | "COMPLETED"
  | "FAILED";

export interface IJudgmentNLP {
  status: NLPStatus;
  startedAt?: Date;
  completedAt?: Date;
  retryCount?: number;
  lastError?: string;
  lockId?: string;
}

export interface IJudgment extends Document {
  title: string;
  year: number;

  status: "UPLOADED" | "PROCESSING" | "COMPLETED" | "FAILED";

  category?: string | null;
  subCategory?: string | null;

  nlp: IJudgmentNLP;

  gridfsFileId: mongoose.Types.ObjectId;
  uploadedAt: Date;
}

const JudgmentSchema = new Schema<IJudgment>({
  title: { type: String, required: true },
  year: { type: Number, required: true },

  status: {
    type: String,
    enum: ["UPLOADED", "PROCESSING", "COMPLETED", "FAILED"],
    default: "UPLOADED",
    index: true,
  },

  category: {
    type: String,
    index: true,
    default: null,
  },

  subCategory: {
    type: String,
    index: true,
    default: null,
  },

  /**
   * NLP lifecycle state
   */
  nlp: {
    status: {
      type: String,
      enum: ["PENDING", "RUNNING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true,
    },
    startedAt: { type: Date },
    completedAt: { type: Date },
    retryCount: { type: Number, default: 0 },
    lastError: { type: String },
    lockId: { type: String },
  },

  gridfsFileId: {
    type: Schema.Types.ObjectId,
    required: true,
  },

  uploadedAt: {
    type: Date,
    default: Date.now,
    index: true,
  },
});

export const Judgment =
  mongoose.models.Judgment ||
  mongoose.model<IJudgment>("Judgment", JudgmentSchema);
