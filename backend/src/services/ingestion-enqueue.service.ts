import JudgmentIngestion from "../models/JudgmentIngestion";

/**
 * Move ingestions from UPLOADED → QUEUED
 */
export async function enqueueIngestions(ingestionIds: string[]) {
  if (!ingestionIds.length) return;

  await JudgmentIngestion.updateMany(
    {
      _id: { $in: ingestionIds },
      status: "UPLOADED",
    },
    {
      $set: {
        status: "QUEUED",
        queuedAt: new Date(),
      },
    }
  );
}
