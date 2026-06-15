import mongoose, { Schema, Document } from "mongoose";

export interface IAct extends Document {
  title: string;

  documentType: "ACT";

  ingestionId?: mongoose.Types.ObjectId;

  fileName: string;

  pdfPath?: string;
  htmlPath?: string;

  extractedText?: string;

  actYear?: number;

  createdAt: Date;
  updatedAt: Date;
}

const ActSchema = new Schema<IAct>(
  {
    title: {
      type: String,
      required: true,
    },

    documentType: {
      type: String,
      default: "ACT",
    },

    ingestionId: {
      type: Schema.Types.ObjectId,
      ref: "JudgmentIngestion",
    },

    fileName: {
      type: String,
      required: true,
    },

    pdfPath: String,
    htmlPath: String,

    extractedText: String,

    actYear: Number,
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<IAct>(
  "Act",
  ActSchema
);
