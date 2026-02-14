import mongoose, { Schema, Types } from "mongoose";

export interface IJudgment {
  ingestionId?: Types.ObjectId; // optional for legacy records

  summary?: string;
  category?: string;
  subCategory?: string;
  pointsOfLaw?: string[];
  confidence?: number;

  createdBy: Types.ObjectId;

  createdAt: Date;
  updatedAt: Date;
}

const JudgmentSchema = new Schema<IJudgment>(
  {
    ingestionId: {
      type: Schema.Types.ObjectId,
      ref: "JudgmentIngestion",
      required: false, // ⚠️ legacy-safe
    },

    summary: {
      type: String,
      trim: true,
    },

    category: {
      type: String,
      index: true,
    },

    subCategory: {
      type: String,
    },

    pointsOfLaw: {
      type: [String],
      default: [],
    },

    confidence: {
      type: Number,
      min: 0,
      max: 1,
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

/**
 * ✅ ONE judgment per ingestion
 * ✅ sparse allows old records without ingestionId
 */
JudgmentSchema.index(
  { ingestionId: 1 },
  { unique: true, sparse: true }
);

// ✅ SAFE MODEL DEFINITION (prevents OverwriteModelError)
const Judgment =
  mongoose.models.Judgment ||
  mongoose.model<IJudgment>("Judgment", JudgmentSchema);

export default Judgment;
