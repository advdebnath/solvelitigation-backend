import mongoose, { Schema, Document, Types } from "mongoose";

export interface IUploadAudit extends Document {
  jobId?: Types.ObjectId;
  judgmentId?: Types.ObjectId;

  fileName: string;
  action: "UPLOAD_SINGLE" | "UPLOAD_BULK";

  filesCount: number;

  uploadedBy: Types.ObjectId;
  ip?: string;
  userAgent?: string;

  createdAt: Date;
}

const UploadAuditSchema = new Schema<IUploadAudit>(
  {
    jobId: {
      type: Schema.Types.ObjectId,
      ref: "Job",
      index: true,
    },

    judgmentId: {
      type: Schema.Types.ObjectId,
      ref: "Judgment",
      index: true,
    },

    fileName: {
      type: String,
      required: true,
    },

    action: {
      type: String,
      enum: ["UPLOAD_SINGLE", "UPLOAD_BULK"],
      required: true,
    },

    filesCount: {
      type: Number,
      default: 1,
    },

    uploadedBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },

    ip: String,
    userAgent: String,
  },
  {
    timestamps: { createdAt: true, updatedAt: false },
  }
);

export const UploadAudit = mongoose.model<IUploadAudit>(
  "UploadAudit",
  UploadAuditSchema
);
