import mongoose from "mongoose";

const CaseHistorySchema = new mongoose.Schema(
  {
    query: String,
    text: String,
    result: Object,
    createdAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

export default mongoose.model("CaseHistory", CaseHistorySchema);
