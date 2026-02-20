import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpJob } from "../utils/nlpEnqueue";

/**
 * Atomically picks ONE QUEUED ingestion
 * and moves it to PROCESSING
 */
async function processNextQueuedIngestion(): Promise<boolean> {
  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    { $or: [ { status: "QUEUED" }, { status: "FAILED", retryCount: { $lt: 3 } } ] },
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
    const currentRetry = ingestion.retryCount || 0;

    if (currentRetry < 3) {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          status: "QUEUED",
          $inc: { retryCount: 1 },
          error: err?.message || "Failed to enqueue NLP",
        }
      );
      console.log(`🔁 Retrying ingestion ${ingestion._id} (attempt ${currentRetry + 1})`);
    } else {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          status: "FAILED",
          error: err?.message || "Failed to enqueue NLP",
        }
      );
      console.log(`❌ Final failure for ingestion ${ingestion._id}`);
    }
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
