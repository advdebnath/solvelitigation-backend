import mongoose from "mongoose";
import dotenv from "dotenv";
import { processQueuedIngestions } from "../services/ingestionProcessingWorker.service";

dotenv.config();

const MONGO_URI = process.env.MONGO_URI!;
const INTERVAL_MS = 5000; // every 5 seconds

async function startWorker() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("🟢 Ingestion Processing Worker connected to MongoDB");

    setInterval(async () => {
      try {
        await processQueuedIngestions(3);
      } catch (err) {
        console.error("❌ Ingestion processing cycle failed:", err);
      }
    }, INTERVAL_MS);

  } catch (err) {
    console.error("❌ Worker startup failed:", err);
    process.exit(1);
  }
}

startWorker();
