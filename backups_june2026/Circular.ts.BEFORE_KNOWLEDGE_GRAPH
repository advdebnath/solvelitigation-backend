import mongoose, { Schema, Document } from "mongoose";

export interface ICircular extends Document {
  title?: string;
  authority?: string;

  documentType: "CIRCULAR";

  ingestionId?: mongoose.Types.ObjectId;

  fileName: string;

  pdfPath?: string;
  htmlPath?: string;

  extractedText?: string;

  circularDate?: Date;

  createdAt: Date;
  updatedAt: Date;
}

const CircularSchema = new Schema<ICircular>(
  {
    title: String,
    authority: String,

    documentType: {
      type: String,
      default: "CIRCULAR",
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

    circularDate: Date,
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<ICircular>(
  "Circular",
  CircularSchema
);
