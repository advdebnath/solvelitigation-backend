import mongoose, { Schema } from "mongoose";

const CaseContextSchema = new Schema(
  {
    caseId: { type: String, unique: true },

    court: String,
    caseType: String,

    petitioner: String,
    respondent: String,

    advocates: {
      petitioner: String,
      respondent: String
    },

    facts: String,
    grounds: String,
    prayer: String
  },
  { timestamps: true }
);

export default mongoose.models.CaseContext ||
  mongoose.model("CaseContext", CaseContextSchema);
