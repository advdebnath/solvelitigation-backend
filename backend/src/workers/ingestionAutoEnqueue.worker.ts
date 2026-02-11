import mongoose from "mongoose";
import { config } from "dotenv";
import { autoEnqueuePendingIngestions } from "../services/ingestionAutoEnqueue.service";

config();

const MONGO_URI = process.env.MONGO_URI!;
const POLL_INTERVAL_MS = Number(
  process.env.INGESTION_AUTO_ENQUEUE_INTERVAL ?? 5000
);

async function startWorker() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("🟢 Auto-Enqueue Worker connected to MongoDB");

    setInterval(async () => {
      try {
        await autoEnqueuePendingIngestions();
        // logging is intentionally minimal to avoid noise
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
