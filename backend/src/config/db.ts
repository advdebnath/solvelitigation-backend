import mongoose from "mongoose";

let isConnecting: Promise<typeof mongoose> | null = null;

export async function connectDB() {
  const uri = process.env.MONGODB_URI;

  if (!uri) {
    throw new Error("❌ MONGODB_URI missing");
  }

  if (mongoose.connection.readyState === 1) {
    return mongoose.connection;
  }

  if (isConnecting) {
    return isConnecting;
  }

  console.log("⏳ Connecting to MongoDB...");
  isConnecting = mongoose.connect(uri);

  await isConnecting;

  console.log("✅ Connected to MongoDB");

  return mongoose.connection;
}
