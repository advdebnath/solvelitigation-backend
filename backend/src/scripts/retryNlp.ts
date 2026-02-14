import dotenv from "dotenv";
dotenv.config({ path: "/var/www/solvelitigation/backend/.env.production" });

import mongoose from "mongoose";
import axios from "axios";
import { Judgment } from "../models";

const MONGO_URI =
  process.env.MONGODB_URI || "";

const NLP_URL =
  process.env.NLP_SERVICE_URL || "http://127.0.0.1:8000";

async function connectDB() {
  if (!MONGO_URI) {
    throw new Error("MongoDB URI not found in env");
  }

  await mongoose.connect(MONGO_URI);
  console.log("✅ retryNlp connected to MongoDB");
}

async function retryNlp() {
  console.log("🔄 NLP retry job started");

  await connectDB();

  const pending = await Judgment.find({
    "nlpStatus": "PENDING",
  }).limit(20);

  if (pending.length === 0) {
    console.log("ℹ️ No pending NLP jobs found");
    process.exit(0);
  }

  for (const j of pending) {
    try {
      await axios.post(`${NLP_URL}/enqueue`, {
        jobId: j._id.toString(),
      });

      console.log(`🔁 Requeued NLP job: ${j._id}`);
    } catch (err: any) {
      console.error(`❌ Failed to enqueue ${j._id}:`, err.message);
    }
  }

  console.log("✅ NLP retry job finished");
  process.exit(0);
}

retryNlp().catch((err) => {
  console.error("❌ NLP retry job failed:", err);
  process.exit(1);
});
