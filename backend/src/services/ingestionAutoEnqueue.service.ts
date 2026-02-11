import JudgmentIngestion from "../models/JudgmentIngestion";
import { enqueueNlpJob } from "../utils/nlpEnqueue";

/**
 * Enqueue NLP for a single ingestion
 */
export async function enqueueNlpForIngestion(ingestionId: string): Promise<void> {
  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    { _id: ingestionId, nlpStatus: "PENDING" },
    { nlpStatus: "QUEUED" },
    { new: true }
  );

  if (!ingestion) return;

  await enqueueNlpJob({
    ingestionId: ingestion._id.toString(),
    pdfPath: ingestion.file.relativePath,
  });
}

/**
 * Auto-enqueue all pending ingestions (worker use)
 */
export async function autoEnqueuePendingIngestions(): Promise<number> {
  const pendings = await JudgmentIngestion.find({
    nlpStatus: "PENDING",
  }).limit(5);

  let processed = 0;

  for (const ingestion of pendings) {
    await enqueueNlpForIngestion(ingestion._id.toString());
    processed++;
  }

  return processed;
}
