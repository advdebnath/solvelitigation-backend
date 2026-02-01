import mongoose, { Schema, Document } from "mongoose";
export interface IJudgment {
  title?: string;
  court?: string;
  year?: number;

  // ✅ ADD THESE

status: {
  type: String,
  enum: ["UPLOADED", "PROCESSING", "COMPLETED", "FAILED"],
  default: "UPLOADED",
},

nlp: {
  status: {
    type: String,
    enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
    default: "PENDING",
  },
  pointsOfLaw: {
    type: [String],
    default: [],
  },
  acts: {
    type: [String],
    default: [],
  },
},


  uploadedBy?: any;
  uploadedAt?: Date;
}


const JudgmentSchema = new Schema<IJudgment>({
  title: { type: String, required: true },
  court: { type: String, required: true },
  year: { type: Number, required: true },
  gridfsFileId: { type: Schema.Types.ObjectId, required: true },
  originalFileName: { type: String, required: true },
  uploadedBy: { type: Schema.Types.ObjectId, required: true },
  uploadedAt: { type: Date, default: Date.now },

nlp: {
  status: {
    type: String,
    enum: ["PENDING", "PROCESSING", "DONE", "FAILED"],
    default: "PENDING",
  },
  pointsOfLaw: { type: [String], default: [] },
  acts: { type: [String], default: [] },
},
status: {
  type: String,
  enum: ["UPLOADED", "PROCESSED"],
  default: "UPLOADED",
},


});

export const Judgment = mongoose.model<IJudgment>(
  "Judgment",
  JudgmentSchema
);
