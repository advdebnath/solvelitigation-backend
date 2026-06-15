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

  authority?: string;

  effectiveDate?: Date;

  checksum?: string;

  sourceDocumentId?: mongoose.Types.ObjectId;

  actReferences?: string[];

  ruleReferences?: string[];

  relatedJudgments?: mongoose.Types.ObjectId[];

  relatedActs?: mongoose.Types.ObjectId[];

  relatedRules?: mongoose.Types.ObjectId[];

  relatedNotifications?: mongoose.Types.ObjectId[];

  relatedCirculars?: mongoose.Types.ObjectId[];

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

    authority: String,

    effectiveDate: Date,

    checksum: String,

    sourceDocumentId: {
      type: Schema.Types.ObjectId,
      ref: "JudgmentIngestion",
    },

    actReferences: [String],

    ruleReferences: [String],

    relatedJudgments: [{
      type: Schema.Types.ObjectId,
      ref: "Judgment",
    }],

    relatedActs: [{
      type: Schema.Types.ObjectId,
      ref: "Act",
    }],

    relatedRules: [{
      type: Schema.Types.ObjectId,
      ref: "Rule",
    }],

    relatedNotifications: [{
      type: Schema.Types.ObjectId,
      ref: "Notification",
    }],

    relatedCirculars: [{
      type: Schema.Types.ObjectId,
      ref: "Circular",
    }],
  },
  {
    timestamps: true,
  }
);

RuleSchema.index({ title: 1 });

RuleSchema.index({ authority: 1 });

RuleSchema.index({ effectiveDate: 1 });

RuleSchema.index({ checksum: 1 });

RuleSchema.index({ documentType: 1 });

export default mongoose.model<IRule>(
  "Rule",
  RuleSchema
);
