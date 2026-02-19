import dotenv from "dotenv";

// Load production env explicitly
dotenv.config({ path: ".env.production" });

import mongoose from "mongoose";
import { autoEnqueuePendingIngestions } from "../services/ingestionAutoEnqueue.service";

const MONGO_URI = process.env.MONGO_URI!;
const POLL_INTERVAL_MS = Number(
  process.env.INGESTION_AUTO_ENQUEUE_INTERVAL ?? 5000
);

async function startWorker() {
  try {
    if (!MONGO_URI) {
      throw new Error("MONGO_URI is not defined");
    }

    console.log("🔌 Connecting to MongoDB...");
    await mongoose.connect(MONGO_URI);

    console.log("🟢 Auto-Enqueue Worker connected to MongoDB");

    setInterval(async () => {
      try {
        await autoEnqueuePendingIngestions();
      } catch (err) {
        console.error("❌ Auto-enqueue cycle failed:", err);
      }
    }, POLL_INTERVAL_MS);

  } catch (err) {
    console.error("❌ Worker startup failed:", err);
    process.exit(1);
  }
}

startWorker();
