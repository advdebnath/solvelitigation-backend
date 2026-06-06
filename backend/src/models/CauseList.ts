import mongoose, { Schema, Document } from "mongoose";

export interface ICauseList extends Document {
  title?: string;
  court?: string;
  documentType: "CAUSE_LIST";

  ingestionId?: mongoose.Types.ObjectId;

  fileName: string;
  pdfPath?: string;
  htmlPath?: string;

  extractedText?: string;

  causeListDate?: Date;

  createdAt: Date;
  updatedAt: Date;
}

const CauseListSchema = new Schema<ICauseList>(
  {
    title: String,
    court: String,

    documentType: {
      type: String,
      default: "CAUSE_LIST",
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

    causeListDate: Date,
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<ICauseList>(
  "CauseList",
  CauseListSchema
);
