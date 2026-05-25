import mongoose, { Schema } from "mongoose";

const VolumeSchema = new Schema(
  {
    year: { type: Number, required: true },
    volume: { type: Number, required: true },
    currentPage: { type: Number, default: 1 },
  },
  { timestamps: true }
);

// 🔥 UNIQUE per year + volume
VolumeSchema.index({ year: 1, volume: 1 }, { unique: true });

export default mongoose.model("Volume", VolumeSchema);
