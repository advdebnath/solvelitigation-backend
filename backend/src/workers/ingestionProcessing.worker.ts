import { config } from "dotenv";
import { connectDB } from "../config/db";
import { processQueuedIngestions } from "../services/ingestionProcessingWorker.service";

config();

const POLL_INTERVAL_MS = Number(
  process.env.INGESTION_POLL_INTERVAL_MS ?? 5000
);

async function startWorker() {
  try {
    await connectDB();
    console.log("🟢 Ingestion Processing Worker started");

    setInterval(async () => {
      try {
        const processed = await processQueuedIngestions();
        if (processed > 0) {
          console.log(`🚀 Processed ${processed} ingestion(s)`);
        }
      } catch (err) {
        console.error("❌ Processing cycle failed:", err);
      }
    }, POLL_INTERVAL_MS);

  } catch (err) {
    console.error("❌ Worker startup failed:", err);
  }
}

startWorker();
