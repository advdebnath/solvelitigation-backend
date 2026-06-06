import logger from "../utils/logger";
import JudgmentIngestion from "../models/JudgmentIngestion";

export async function enqueueNlpForIngestion(
  ingestionId: string
): Promise<void> {
  const ingestion = await JudgmentIngestion.findById(ingestionId);
  if (!ingestion) return;

  ingestion.status = "QUEUED";
  await ingestion.save();
}

export async function autoEnqueuePendingIngestions(): Promise<number> {
  try {
    const processingCount = await JudgmentIngestion.countDocuments({
      status: "PROCESSING",
    });

    if (processingCount > 50) {
      logger.info("⚠ Throttle active: Too many PROCESSING items");
      return 0;
    }

    const ingestions = await JudgmentIngestion.find({
      status: "UPLOADED",
    })
      .limit(20)
      .sort({ createdAt: 1 });

    if (!ingestions.length) {
      return 0;
    }

    let processed = 0;

    for (const ingestion of ingestions) {
      ingestion.status = "QUEUED";
      await ingestion.save();
      processed++;
    }

    const queueDepth = await JudgmentIngestion.countDocuments({
      status: { $in: ["QUEUED", "PROCESSING"] },
    });

    logger.info(
      `🚀 Auto-enqueued: ${processed} | Queue depth: ${queueDepth}`
    );

    return processed;
  } catch (error) {
    logger.error("❌ Auto-enqueue error:", error);
    return 0;
  }
}
