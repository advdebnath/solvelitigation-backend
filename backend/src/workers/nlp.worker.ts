import mongoose from "mongoose";
import JudgmentIngestion from "../models/JudgmentIngestion";

/**
 * Mark ingestion as PROCESSING
 */
async function markProcessing(ingestionId: string) {
  if (!mongoose.Types.ObjectId.isValid(ingestionId)) return;

  await JudgmentIngestion.updateOne(
    { _id: ingestionId, status: "QUEUED" },
    {
      status: "PROCESSING",
      processingAt: new Date(),
    }
  );
}

/**
 * Mark ingestion as COMPLETED
 */
async function markCompleted(ingestionId: string, judgmentId?: string) {
  if (!mongoose.Types.ObjectId.isValid(ingestionId)) return;

  await JudgmentIngestion.updateOne(
    { _id: ingestionId },
    {
      status: "COMPLETED",
      completedAt: new Date(),
      ...(judgmentId ? { judgmentId } : {}),
      error: undefined,
    }
  );
}

/**
 * Mark ingestion as FAILED
 */
async function markFailed(ingestionId: string, err: unknown) {
  if (!mongoose.Types.ObjectId.isValid(ingestionId)) return;

  const message =
    err instanceof Error ? err.message : "NLP processing failed";

  await JudgmentIngestion.updateOne(
    { _id: ingestionId },
    {
      status: "FAILED",
      failedAt: new Date(),
      error: message,
    }
  );
}

/**
 * NLP Worker entry point
 */
export async function nlpWorker(ingestionId: string) {
  await markProcessing(ingestionId);

  try {
    const ingestion = await JudgmentIngestion.findById(ingestionId);

    if (!ingestion) {
      throw new Error("Ingestion not found");
    }

    console.log("🧠 NLP processing started for ingestion:", ingestion._id);

    // 🔹 NLP execution will be implemented in the next phase 🔹
    // Example (future):
    // const judgmentId = await runNlpPipeline(ingestion.file.relativePath);

    await markCompleted(ingestionId /*, judgmentId */);
  } catch (err) {
    await markFailed(ingestionId, err);
    throw err;
  }
}
