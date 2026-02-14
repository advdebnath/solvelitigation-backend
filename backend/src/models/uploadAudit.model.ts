import mongoose, { Schema, Document, Model } from "mongoose";

export interface IUploadAudit extends Document {
  action: "UPLOAD" | "BULK_UPLOAD" | "DELETE" | "REPROCESS";
  status: "SUCCESS" | "FAILED" | "DRY_RUN";
  fileName: string;
  filePath?: string;
  courtType?: string;
  year?: string;
  error?: string;
  uploadedBy: mongoose.Types.ObjectId;
  ip?: string;
  userAgent?: string;
  createdAt: Date;
}

const UploadAuditSchema = new Schema<IUploadAudit>(
  {
    action: {
      type: String,
      enum: ["UPLOAD", "BULK_UPLOAD", "DELETE", "REPROCESS"],
      required: true,
      index: true,
    },

    status: {
      type: String,
      enum: ["SUCCESS", "FAILED", "DRY_RUN"],
      required: true,
      index: true,
    },

    fileName: {
      type: String,
      required: true,
    },

    filePath: {
      type: String,
    },

    courtType: {
      type: String,
      index: true,
    },

    year: {
      type: String,
      index: true,
    },

    error: {
      type: String,
    },

    uploadedBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },

    ip: {
      type: String,
    },

    userAgent: {
      type: String,
    },
  },
  {
    timestamps: { createdAt: true, updatedAt: false },
  }
);

export const UploadAudit: Model<IUploadAudit> =
  mongoose.models.UploadAudit ||
  mongoose.model<IUploadAudit>("UploadAudit", UploadAuditSchema);
