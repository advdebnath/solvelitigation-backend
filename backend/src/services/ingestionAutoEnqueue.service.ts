import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpJob } from "../utils/nlpEnqueue";

/**
 * Move QUEUED → PROCESSING and trigger NLP
 */
export async function enqueueNlpForIngestion(
  ingestionId: string
): Promise<void> {
  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    { _id: ingestionId, status: "QUEUED" },
    { status: "PROCESSING", processingStartedAt: new Date() },
    { new: true }
  );

  if (!ingestion) return;

  await enqueueNlpJob(ingestion._id.toString());
}

/**
 * Auto-enqueue UPLOADED ingestions
 * Moves: UPLOADED → QUEUED
 * Does NOT directly call NLP
 */
export async function autoEnqueuePendingIngestions(): Promise<number> {
  const uploads = await JudgmentIngestion.find({
    status: "UPLOADED",
  }).limit(5);

  let processed = 0;

  for (const ingestion of uploads) {
    const updated = await JudgmentIngestion.findOneAndUpdate(
      { _id: ingestion._id, status: "UPLOADED" },
      {
        status: "QUEUED",
        queuedAt: new Date(),
      },
      { new: true }
    );

    if (updated) {
      processed++;
    }
  }

  return processed;
}
