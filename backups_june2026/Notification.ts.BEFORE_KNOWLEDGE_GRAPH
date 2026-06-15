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
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<INotification>(
  "Notification",
  NotificationSchema
);
