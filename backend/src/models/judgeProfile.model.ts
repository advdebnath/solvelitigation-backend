import mongoose from "mongoose";

const JudgeProfileSchema = new mongoose.Schema({
  name: { type: String, required: true, unique: true },

  totalCases: { type: Number, default: 0 },
  allowed: { type: Number, default: 0 },
  rejected: { type: Number, default: 0 },

  bailGranted: { type: Number, default: 0 },
  bailRejected: { type: Number, default: 0 },

  precedentHeavy: { type: Number, default: 0 },

}, { timestamps: true });

export default mongoose.model("JudgeProfile", JudgeProfileSchema);
