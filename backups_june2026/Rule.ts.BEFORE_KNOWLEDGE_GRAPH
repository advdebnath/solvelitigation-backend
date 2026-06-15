import mongoose, { Schema, Document } from "mongoose";

export interface IRule extends Document {
  title: string;

  documentType: "RULE";

  ingestionId?: mongoose.Types.ObjectId;

  parentAct?: mongoose.Types.ObjectId;

  fileName: string;

  pdfPath?: string;
  htmlPath?: string;

  extractedText?: string;

  ruleYear?: number;

  createdAt: Date;
  updatedAt: Date;
}

const RuleSchema = new Schema<IRule>(
  {
    title: {
      type: String,
      required: true,
    },

    documentType: {
      type: String,
      default: "RULE",
    },

    ingestionId: {
      type: Schema.Types.ObjectId,
      ref: "JudgmentIngestion",
    },

    parentAct: {
      type: Schema.Types.ObjectId,
      ref: "Act",
    },

    fileName: {
      type: String,
      required: true,
    },

    pdfPath: String,
    htmlPath: String,

    extractedText: String,

    ruleYear: Number,
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<IRule>(
  "Rule",
  RuleSchema
);
