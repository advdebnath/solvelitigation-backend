import mongoose, { Schema, Document } from "mongoose";

export interface INotification extends Document {
  title?: string;
  authority?: string;

  documentType: "NOTIFICATION";

  ingestionId?: mongoose.Types.ObjectId;

  fileName: string;

  pdfPath?: string;
  htmlPath?: string;

  extractedText?: string;

  notificationDate?: Date;

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

const NotificationSchema = new Schema<INotification>(
  {
    title: String,
    authority: String,

    documentType: {
      type: String,
      default: "NOTIFICATION",
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

    notificationDate: Date,

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

NotificationSchema.index({ title: 1 });

NotificationSchema.index({ authority: 1 });

NotificationSchema.index({ effectiveDate: 1 });

NotificationSchema.index({ checksum: 1 });

NotificationSchema.index({ documentType: 1 });

export default mongoose.model<INotification>(
  "Notification",
  NotificationSchema
);
