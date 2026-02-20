import JudgmentIngestion from "../models/JudgmentIngestion";

export async function recoverStuckIngestions() {
  console.log("🛟 Running ingestion recovery sweep...");

  const timeoutMinutes = 30;
  const cutoff = new Date(Date.now() - timeoutMinutes * 60 * 1000);

  const stuckIngestions = await JudgmentIngestion.find({
    status: "PROCESSING",
    updatedAt: { $lt: cutoff },
  });

  if (!stuckIngestions.length) {
    console.log("✅ No stuck ingestions found");
    return;
  }

  let recovered = 0;
  let permanentlyFailed = 0;

  for (const ingestion of stuckIngestions) {
    ingestion.retryCount = (ingestion.retryCount || 0) + 1;

    if (ingestion.retryCount >= 3) {
      ingestion.status = "PERMANENT_FAILURE";
      ingestion.permanentFailureAt = new Date();
      permanentlyFailed++;
    } else {
      ingestion.status = "QUEUED";
      recovered++;
    }

    await ingestion.save();
  }

  console.log(
    `🛟 Recovery summary → Re-queued: ${recovered}, Permanent: ${permanentlyFailed}`
  );
}
