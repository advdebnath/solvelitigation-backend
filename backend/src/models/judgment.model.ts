import mongoose, { Schema, Document } from "mongoose";

export type NLPStatus = "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";

export interface IJudgmentNLP {
  status: NLPStatus;
  pointsOfLaw: string[];
  acts: string[];
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

  nlp: {
    status: {
      type: String,
      enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true,
    },
    pointsOfLaw: { type: [String], default: [] },
    acts: { type: [String], default: [] },
  },

  gridfsFileId: {
    type: Schema.Types.ObjectId,
    required: true,
  },

  uploadedAt: { type: Date, default: Date.now, index: true },
});

export const Judgment =
  mongoose.models.Judgment ||
  mongoose.model<IJudgment>("Judgment", JudgmentSchema);
