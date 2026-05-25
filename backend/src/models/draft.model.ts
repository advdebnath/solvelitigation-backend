import mongoose, { Schema, Document } from "mongoose";

export interface IDraft extends Document {
  caseId: string;
  court: string; // District | High Court | Supreme Court
  type: string;  // petition | stay | delay | notice etc.

  title: string;
  content: string;

  isFinal: boolean;
  version: number;

  createdBy: mongoose.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const DraftSchema = new Schema<IDraft>(
  {
    caseId: { type: String, index: true },

    court: {
      type: String,
      enum: ["DISTRICT", "HIGH", "SUPREME"],
      required: true,
      index: true
    },

    type: {
      type: String,
      required: true,
      index: true
    },

    title: {
      type: String,
      trim: true
    },

    content: {
      type: String,
      required: true
    },

    isFinal: {
      type: Boolean,
      default: false
    },

    version: {
      type: Number,
      default: 1
    },

    createdBy: {
      type: Schema.Types.ObjectId,
      ref: "User"
    }
  },
  { timestamps: true }
);

// 🔥 INDEX (IMPORTANT)
DraftSchema.index({ caseId: 1, type: 1, version: -1 });

export default mongoose.models.Draft ||
  mongoose.model<IDraft>("Draft", DraftSchema);
