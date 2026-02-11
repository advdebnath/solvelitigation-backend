import { Request, Response } from "express";
import mongoose from "mongoose";
import JudgmentIngestion from "../../models/JudgmentIngestion";
import { enqueueNlpForIngestion } from "../../services/ingestionAutoEnqueue.service";

/**
 * POST /ingestion/:id/enqueue
 * Superadmin manual enqueue
 */
export async function enqueueIngestion(req: Request, res: Response) {
  const { id } = req.params;

  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).json({ message: "Invalid ingestion id" });
  }

  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    {
      _id: id,
      status: { $in: ["UPLOADED", "FAILED"] },
    },
    {
      status: "QUEUED",
      queuedAt: new Date(),
      error: undefined,
    },
    { new: true }
  );

  if (!ingestion) {
    return res.status(404).json({ message: "Ingestion not eligible for enqueue" });
  }

  await enqueueNlpForIngestion(ingestion._id.toString());

  res.json({
    success: true,
    ingestionId: ingestion._id,
    status: ingestion.status,
  });
}

/**
 * POST /ingestion/:id/retry
 * FAILED → QUEUED
 */
export async function retryIngestion(req: Request, res: Response) {
  const { id } = req.params;

  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).json({ message: "Invalid ingestion id" });
  }

  const ingestion = await JudgmentIngestion.findOneAndUpdate(
    {
      _id: id,
      status: "FAILED",
    },
    {
      status: "QUEUED",
      queuedAt: new Date(),
      $inc: { retryCount: 1 },
      error: undefined,
    },
    { new: true }
  );

  if (!ingestion) {
    return res.status(404).json({ message: "Only FAILED ingestions can be retried" });
  }

  await enqueueNlpForIngestion(ingestion._id.toString());

  res.json({
    success: true,
    ingestionId: ingestion._id,
    retryCount: ingestion.retryCount,
  });
}
