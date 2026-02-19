import  JudgmentIngestion  from "../models/JudgmentIngestion";

export async function recoverStuckIngestions() {
  console.log("🛟 Running ingestion recovery sweep...");

  const timeoutMinutes = 30;
  const cutoff = new Date(Date.now() - timeoutMinutes * 60 * 1000);

  const stuck = await JudgmentIngestion.updateMany(
    {
      status: "PROCESSING",
      updatedAt: { $lt: cutoff },
    },
    {
      $set: { status: "QUEUED" },
      $inc: { retryCount: 1 },
    }
  );

  if (stuck.modifiedCount > 0) {
    console.log(`♻️ Recovered ${stuck.modifiedCount} stuck ingestions`);
  } else {
    console.log("✅ No stuck ingestions found");
  }
}
