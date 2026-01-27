import mongoose from "mongoose";

export async function connectDB() {
  const uri = process.env.MONGODB_URI;

  if (!uri) {
    throw new Error("❌ MONGODB_URI missing");
  }

  if (mongoose.connection.readyState === 1) {
    return mongoose.connection;
  }

  console.log("⏳ Connecting to MongoDB...");
  await mongoose.connect(uri);
  console.log("✅ Connected to MongoDB");

  return mongoose.connection;
}
