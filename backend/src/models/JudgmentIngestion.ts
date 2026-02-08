import mongoose, { Schema, Document } from "mongoose";

export interface IJudgmentIngestion extends Document {
  source: string;
  uploadType: "single" | "bulk";
  pathMeta?: {
    year: number;
    month: number;
    date: number;
  };
  file: {
    originalName: string;
    size: number;
    sha256: string;
    gridfsFileId: mongoose.Types.ObjectId;
  };
  status:
    | "UPLOADED"
    | "REGISTERED"
    | "NLP_PENDING"
    | "NLP_PROCESSING"
    | "COMPLETED"
    | "FAILED";
  errorReason?: string;
  createdBy: mongoose.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const JudgmentIngestionSchema = new Schema<IJudgmentIngestion>(
  {
    source: { type: String, required: true },
    uploadType: { type: String, enum: ["single", "bulk"], required: true },

    pathMeta: {
      year: Number,
      month: Number,
      date: Number,
    },

    file: {
      originalName: { type: String, required: true },
      size: { type: Number, required: true },
      sha256: { type: String, required: true },
      gridfsFileId: {
        type: Schema.Types.ObjectId,
        required: true,
      },
    },

    status: {
      type: String,
      enum: [
        "UPLOADED",
        "REGISTERED",
        "NLP_PENDING",
        "NLP_PROCESSING",
        "COMPLETED",
        "FAILED",
      ],
      default: "UPLOADED",
    },

    errorReason: String,
    createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
  },
  { timestamps: true }
);

export default mongoose.model<IJudgmentIngestion>(
  "JudgmentIngestion",
  JudgmentIngestionSchema
);
