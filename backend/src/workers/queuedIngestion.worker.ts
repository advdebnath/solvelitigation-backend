import dotenv from "dotenv";
import mongoose from "mongoose";
import { connectDB } from "../config/db";
import { processQueuedIngestions } from "../services/ingestionProcessingWorker.service";

dotenv.config();

const POLL_INTERVAL_MS = 5000;

async function startWorker() {
  try {
    console.log("⏳ Connecting to MongoDB...");
    await connectDB();
    console.log("🟢 Ingestion Processing Worker connected to MongoDB");

    async function poll() {
      try {
        await processQueuedIngestions();
      } catch (err) {
        console.error("❌ Processing cycle failed:", err);
      } finally {
        setTimeout(poll, POLL_INTERVAL_MS);
      }
    }

    poll();

  } catch (err) {
    console.error("❌ Worker startup failed:", err);
    process.exit(1);
  }
}

startWorker();
