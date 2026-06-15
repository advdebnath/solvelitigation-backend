import mongoose, { Schema, Document } from "mongoose";

export type IngestionStatus =
  | "UPLOADED"
  | "QUEUED"
  | "PROCESSING"
  | "COMPLETED"
  | "FAILED"
  | "PERMANENT_FAILURE";

export type DocumentType =
  | "JUDGMENT"
  | "ACT"
  | "RULE"
  | "NOTIFICATION"
  | "CIRCULAR";

export type IngestionStage =
  | "UPLOADED"
  | "QUEUED"
  | "PROCESSING"
  | "NLP"
  | "FINALIZING"
  | "COMPLETED"
  | "FAILED";

export interface IJudgmentIngestion extends Document {
  source: string;
  uploadType: "single" | "folder";

  fileName: string;
  documentType: DocumentType;

  progress: number;
  stage: IngestionStage;

  file: {
    originalName: string;
    relativePath: string;
    size: number;
    sha256: string;
    gridfsFileId?: mongoose.Types.ObjectId;
  };

  extractedMeta?: {
    year?: number;
    month?: number;
    date?: number;
  };

  status: IngestionStatus;

  error?: string | null;
  lastErrorAt?: Date;

  retryCount: number;
  maxRetries: number;

  isLocked: boolean;
  processingNode?: string;

  queuedAt?: Date;
  processingAt?: Date;
  completedAt?: Date;
  failedAt?: Date;
  permanentFailureAt?: Date;

  // 🔥 CONTROL FIELDS
  nlpProcessed?: boolean;
  nlpQueued?: boolean;        // ✅ NEW (CRITICAL)
  isCompleted?: boolean;
  nlpUpdatedAt?: Date;

  judgmentId?: mongoose.Types.ObjectId;

  createdBy?: mongoose.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const JudgmentIngestionSchema = new Schema<IJudgmentIngestion>(
  {
    source: { type: String },

    uploadType: {
      type: String,
      enum: ["single", "folder"],
    },

    fileName: {
      type: String,
      required: true,
    },

    documentType: {
      type: String,
      enum: ["JUDGMENT", "ACT", "RULE", "NOTIFICATION", "CIRCULAR"],
      default: "JUDGMENT",
    },

    progress: {
      type: Number,
      default: 0,
      min: 0,
      max: 100,
    },

    stage: {
      type: String,
      enum: [
        "UPLOADED",
        "QUEUED",
        "PROCESSING",
        "NLP",
        "FINALIZING",
        "COMPLETED",
        "FAILED",
      ],
      default: "UPLOADED",
    },

    file: {
      originalName: { type: String, required: true },
      relativePath: { type: String, required: true },
      size: Number,
      sha256: { type: String },
      gridfsFileId: { type: Schema.Types.ObjectId },
    },

    extractedMeta: {
      year: Number,
      month: Number,
      date: Number,
    },

    status: {
      type: String,
      enum: [
        "UPLOADED",
        "QUEUED",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        "PERMANENT_FAILURE",
      ],
      default: "UPLOADED",
    },

    error: {
      type: String,
      default: null,
    },

    lastErrorAt: Date,

    retryCount: { type: Number, default: 0 },
    maxRetries: { type: Number, default: 3 },

    isLocked: {
      type: Boolean,
      default: false,
    },

    processingNode: String,

    queuedAt: Date,
    processingAt: Date,
    completedAt: Date,
    failedAt: Date,
    permanentFailureAt: Date,

    // 🔥 CONTROL FLAGS
    nlpProcessed: {
      type: Boolean,
      default: false,
    },

    nlpQueued: {               // ✅ CRITICAL FIX
      type: Boolean,
      default: false,
    },

    isCompleted: {
      type: Boolean,
      default: false,
    },

    nlpUpdatedAt: Date,

    judgmentId: {
      type: Schema.Types.ObjectId,
      ref: "Judgment",
    },

    createdBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
    },
  },
  { timestamps: true }
);

//
// 🔥 INDEXES
//

JudgmentIngestionSchema.index({ status: 1, isLocked: 1 });
JudgmentIngestionSchema.index({ documentType: 1, status: 1 });
JudgmentIngestionSchema.index({ "file.sha256": 1 });
JudgmentIngestionSchema.index({ fileName: 1 });
JudgmentIngestionSchema.index({ source: 1 });
JudgmentIngestionSchema.index({ judgmentId: 1 });
JudgmentIngestionSchema.index({ createdBy: 1 });
JudgmentIngestionSchema.index({ isLocked: 1 });

// 🔥 IMPORTANT: prevents duplicate enqueue race
JudgmentIngestionSchema.index({ nlpQueued: 1, status: 1 });

export default mongoose.model<IJudgmentIngestion>(
  "JudgmentIngestion",
  JudgmentIngestionSchema
);
