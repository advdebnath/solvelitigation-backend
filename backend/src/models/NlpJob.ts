import mongoose, { Schema } from "mongoose";

const NlpJobSchema = new Schema(
  {
    judgmentId: {
      type: Schema.Types.ObjectId,
      ref: "Judgment",
      required: true,
      index: true
    },
    ingestionId: {
      type: Schema.Types.ObjectId,
      ref: "JudgmentIngestion",
      required: true,
      index: true
    },
    status: {
      type: String,
      enum: ["PENDING", "PROCESSING", "COMPLETED", "FAILED"],
      default: "PENDING",
      index: true
    },
    error: String
  },
  { timestamps: true, collection: "nlpjobs" }
);

const NlpJob =
  mongoose.models.NlpJob ||
  mongoose.model("NlpJob", NlpJobSchema);

export default NlpJob;
