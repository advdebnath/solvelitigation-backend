import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpJob } from "../utils/nlpEnqueue";

/**
 * Atomically picks ONE QUEUED ingestion
 * and moves it to PROCESSING
 */
async function processNextQueuedIngestion(): Promise<boolean> {
  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    { status: "QUEUED" },
    { status: "PROCESSING", startedAt: new Date() },
    { sort: { createdAt: 1 }, new: true }
  );

  if (!ingestion) {
    return false;
  }

  try {
    await enqueueNlpJob(ingestion._id.toString());
    return true;
  } catch (err: any) {
    await JudgmentIngestion.updateOne(
      { _id: ingestion._id },
      {
        status: "FAILED",
        error: err?.message || "Failed to enqueue NLP",
      }
    );
    return false;
  }
}

/**
 * Batch processor
 */
export async function processQueuedIngestions(
  limit = 3
): Promise<number> {
  let processedCount = 0;

  for (let i = 0; i < limit; i++) {
    const processed = await processNextQueuedIngestion();
    if (!processed) break;
    processedCount++;
  }

  return processedCount;
}
