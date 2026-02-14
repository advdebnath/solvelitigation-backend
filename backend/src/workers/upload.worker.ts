import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpForIngestion } from "../services/ingestionAutoEnqueue.service";

export async function runUploadWorker() {
  // 🔍 Find ingestions that should be enqueued
  const ingestions = await JudgmentIngestion.find({
    status: "UPLOADED",
  }).select("_id");

  if (ingestions.length === 0) {
    return;
  }

  for (const ingestion of ingestions) {
    try {
      await enqueueNlpForIngestion(ingestion._id.toString());
    } catch (err) {
      console.error(
        "❌ Failed to auto-enqueue ingestion:",
        ingestion._id.toString(),
        err
      );
    }
  }
}
