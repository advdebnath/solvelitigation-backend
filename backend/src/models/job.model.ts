import { Schema, model, Types } from "mongoose";

export interface IJob {
  type: string;
  payload: any;
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
  progress?: number;
  totalTasks?: number;
  completedTasks?: number;
  createdBy?: Types.ObjectId;
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

const jobSchema = new Schema<IJob>(
  {
    type: { type: String, required: true },
    payload: { type: Schema.Types.Mixed, required: true },

    status: {
      type: String,
      enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true,
    },

    progress: {
      type: Number,
      default: 0,
      min: 0,
      max: 100,
    },

    totalTasks: {
      type: Number,
      default: 0,
    },

    completedTasks: {
      type: Number,
      default: 0,
    },

    createdBy: {
      type: Schema.Types.ObjectId,
      ref: "User",
      index: true,
    },

    error: { type: String },
  },
  { timestamps: true }
);

export const Job = model<IJob>("Job", jobSchema);
