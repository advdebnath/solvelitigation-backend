import mongoose from "mongoose";
import { processQueuedIngestions } from "../services/ingestionProcessingWorker.service";

const POLL_INTERVAL_MS = 5000; // every 5 seconds

async function startWorker() {
  try {
    await mongoose.connect(process.env.MONGO_URI!);
    console.log("🟢 Ingestion Processing Worker connected to MongoDB");

    setInterval(async () => {
      try {
        const processed = await processQueuedIngestions(5);

        if (processed > 0) {
          console.log(`🚀 Processed ${processed} ingestion(s)`);
        }
      } catch (err) {
        console.error("❌ Processing cycle failed:", err);
      }
    }, POLL_INTERVAL_MS);

  } catch (err) {
    console.error("❌ Worker startup failed:", err);
    process.exit(1);
  }
}

startWorker();
