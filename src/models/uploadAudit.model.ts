import { Schema, model, Types } from "mongoose";

export interface IUploadAudit {
  jobId?: Types.ObjectId;
  uploadedBy: Types.ObjectId;
  role: string;
  courtType: "SUPREME" | "HIGH" | "TRIBUNAL";
  filesCount: number;
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

const uploadAuditSchema = new Schema<IUploadAudit>(
  {
    jobId: {
      type: Schema.Types.ObjectId,
      ref: "Job",
      index: true,
    },
    uploadedBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    role: {
      type: String,
      required: true,
    },
    courtType: {
      type: String,
      enum: ["SUPREME", "HIGH", "TRIBUNAL"],
      required: true,
    },
    filesCount: {
      type: Number,
      required: true,
    },
    status: {
      type: String,
      enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true,
    },
    error: {
      type: String,
    },
  },
  { timestamps: true }
);

export const UploadAudit = model<IUploadAudit>(
  "UploadAudit",
  uploadAuditSchema
);
