import JudgmentIngestion from "../models/JudgmentIngestion";

export type IngestionStatus =
  | "UPLOADED"
  | "REGISTERED"
  | "NLP_PENDING"
  | "NLP_PROCESSING"
  | "COMPLETED"
  | "FAILED";

/**
 * Update ingestion status safely
 */
export async function updateIngestionStatus(
  ingestionId: string,
  status: IngestionStatus,
  errorReason?: string
) {
  const update: any = { status };

  if (errorReason) {
    update.errorReason = errorReason;
  }

  await JudgmentIngestion.findByIdAndUpdate(
    ingestionId,
    update,
    { new: true }
  );
}
