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

ActSchema.index({ title: 1 });

ActSchema.index({ authority: 1 });

ActSchema.index({ effectiveDate: 1 });

ActSchema.index({ checksum: 1 });

ActSchema.index({ documentType: 1 });

export default mongoose.model<IAct>(
  "Act",
  ActSchema
);
