import JudgmentIngestion from "../models/JudgmentIngestion";
import logger from "../utils/logger";

export async function recoverStuckIngestions() {
  logger.info("🛟 Running ingestion recovery sweep...");

  const timeoutMinutes = Number(process.env.INGESTION_TIMEOUT_MINUTES ?? 30);
  const maxRetries = Number(process.env.INGESTION_MAX_RETRIES ?? 3);

  const cutoff = new Date(Date.now() - timeoutMinutes * 60 * 1000);

  const stuckIngestions = await JudgmentIngestion.find({
    status: "PROCESSING",
    updatedAt: { $lt: cutoff },
  });

  if (stuckIngestions.length === 0) {
    logger.info("✅ No stuck ingestions found");
  }

  for (const ingestion of stuckIngestions) {
    if (ingestion.retryCount >= maxRetries) {
      ingestion.status = "FAILED";
      logger.warn("❌ Ingestion permanently failed after max retries", {
        ingestionId: ingestion._id,
        retryCount: ingestion.retryCount,
        maxRetries,
      });
    } else {
      ingestion.status = "QUEUED";
      ingestion.retryCount += 1;
      logger.warn("♻️ Re-queued stuck ingestion", {
        ingestionId: ingestion._id,
        retryCount: ingestion.retryCount,
        maxRetries,
      });
    }

    await ingestion.save();
  }

  // 🔔 FAILED ALERT CHECK
  const failedCount = await JudgmentIngestion.countDocuments({
    status: "FAILED",
  });

  if (failedCount > 0) {
    logger.error("🚨 FAILED INGESTIONS DETECTED", {
      failedCount,
    });
  }
}
