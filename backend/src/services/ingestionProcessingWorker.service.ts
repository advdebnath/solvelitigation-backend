const PROCESSING_TIMEOUT_MS = Number(
  process.env.INGESTION_PROCESSING_TIMEOUT_MS ?? 10 * 60 * 1000
);

import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpJob } from "../utils/nlpEnqueue";

/* ============================================================
   Pick ONE QUEUED ingestion and move to PROCESSING
============================================================ */

async function processNextQueuedIngestion(): Promise<boolean> {
  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    { status: "QUEUED" }, // ✅ Correct status
    {
      $set: {
        status: "PROCESSING",
        processingAt: new Date(),
      },
    },
    {
      sort: { createdAt: 1 },
      new: true,
    }
  );

  if (!ingestion) {
    return false;
  }

  try {
    console.log("📤 Sending to NLP:", {
      ingestionId: ingestion._id.toString(),
    });

    await enqueueNlpJob(ingestion._id.toString());

    return true;
  } catch (err: any) {
    const maxRetries = Number(process.env.INGESTION_MAX_RETRIES ?? 3);
    const currentRetry = ingestion.retryCount || 0;

    if (currentRetry < maxRetries) {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          $set: {
            status: "QUEUED", // retry back to queue
            error: err?.message || "Failed to enqueue NLP",
          },
          $inc: { retryCount: 1 },
        }
      );

      console.log(
        `🔁 Retry scheduled for ingestion ${ingestion._id} (attempt ${
          currentRetry + 1
        })`
      );
    } else {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          $set: {
            status: "FAILED",
            error: err?.message || "Max retries exceeded",
          },
        }
      );

      console.log(`❌ Final failure for ingestion ${ingestion._id}`);
    }

    return false;
  }
}

/* ============================================================
   Recover stuck PROCESSING ingestions
============================================================ */

async function recoverStuckProcessing(): Promise<void> {
  const threshold = new Date(Date.now() - PROCESSING_TIMEOUT_MS);

  const stuckIngestions = await JudgmentIngestion.find({
    status: "PROCESSING",
    processingAt: { $lt: threshold },
  });

  for (const ingestion of stuckIngestions) {
    const maxRetries = Number(process.env.INGESTION_MAX_RETRIES ?? 3);
    const currentRetry = ingestion.retryCount || 0;

    if (currentRetry < maxRetries) {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          $set: {
            status: "QUEUED",
            error: "Auto-recovered from stuck PROCESSING",
          },
          $inc: { retryCount: 1 },
        }
      );

      console.log(`♻️ Auto-recovered stuck ingestion ${ingestion._id}`);
    } else {
      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          $set: {
            status: "FAILED",
            error: "Exceeded max retries after stuck PROCESSING",
          },
        }
      );

      console.log(`❌ Marked permanently failed: ${ingestion._id}`);
    }
  }
}

/* ============================================================
   Main Batch Processor
============================================================ */

export async function processQueuedIngestions(): Promise<number> {
  await recoverStuckProcessing();

  const maxConcurrent = Number(
    process.env.INGESTION_MAX_CONCURRENT ?? 5
  );

  const processingCount = await JudgmentIngestion.countDocuments({
    status: "PROCESSING",
  });

  const availableSlots = Math.max(
    maxConcurrent - processingCount,
    0
  );

  let processedCount = 0;

  for (let i = 0; i < availableSlots; i++) {
    const processed = await processNextQueuedIngestion();
    if (!processed) break;
    processedCount++;
  }

  return processedCount;
}
