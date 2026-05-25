import mongoose, { Schema } from "mongoose";

export interface IActMaster {
  canonicalName: string;      // Full legal name
  shortName?: string;         // IPC, CrPC, etc
  category?: string;          // Civil / Criminal / Tax / Service
  aliases: string[];          // NLP matching
  sectionPattern?: string;    // Regex for section detection
}

const ActMasterSchema = new Schema<IActMaster>(
  {
    canonicalName: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },

    shortName: {
      type: String,
      index: true,
    },

    category: {
      type: String,
      index: true,
    },

    aliases: {
      type: [String],
      default: [],
      index: true,
    },

    sectionPattern: {
      type: String, // e.g. "Section\\s*\\d+"
    },
  },
  { timestamps: true }
);

// 🔥 Text index for smart search
ActMasterSchema.index({
  canonicalName: "text",
  aliases: "text",
  shortName: "text",
});

const ActMaster =
  mongoose.models.ActMaster ||
  mongoose.model<IActMaster>("ActMaster", ActMasterSchema);

export default ActMaster;
