import mongoose, { Schema, Document } from "mongoose";

export interface INlpJob extends Document {
  judgmentId: string;
  pdfPath: string;
  options: Record<string, any>;
  status: "QUEUED" | "PROCESSING" | "COMPLETED" | "FAILED";
  result?: any;
  error?: string;
  createdAt: Date;
}

const NlpJobSchema = new Schema<INlpJob>(
  {
    judgmentId: { type: String, required: true },
    pdfPath: { type: String, required: true },
    options: { type: Schema.Types.Mixed },
    status: {
      type: String,
      enum: ["QUEUED", "PROCESSING", "COMPLETED", "FAILED"],
      default: "QUEUED",
    },
    result: Schema.Types.Mixed,
    error: String,
  },
  { timestamps: true }
);

export const NlpJob =
  mongoose.models.NlpJob || mongoose.model<INlpJob>("NlpJob", NlpJobSchema);
