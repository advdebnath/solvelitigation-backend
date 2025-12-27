import { Job } from "@/models/job.model";
import { processUploadJob } from "./upload.worker";

/**
 * Serial job processor with locking & recovery
 */
export const processJobsSerially = async () => {
  const now = new Date();

  /**
   * 1️⃣ Recover stuck jobs (PROCESSING > 10 minutes)
   */
  await Job.updateMany(
    {
      status: "PROCESSING",
      updatedAt: { $lt: new Date(Date.now() - 10 * 60 * 1000) },
    },
    {
      $set: {
        status: "FAILED",
        error: "Job timed out",
      },
    }
  );

  /**
   * 2️⃣ Atomically lock ONE pending job
   */
  const job = await Job.findOneAndUpdate(
    { status: "PENDING" },
    {
      status: "PROCESSING",
      updatedAt: now,
    },
    { new: true }
  );

  if (!job) return;

  try {
    switch (job.type) {
      case "UPLOAD_JUDGMENTS":
        await processUploadJob(job._id.toString());
        break;

      default:
        throw new Error(`Unknown job type: ${job.type}`);
    }

    /**
     * 3️⃣ Mark success
     */
    await Job.findByIdAndUpdate(job._id, {
      status: "COMPLETED",
      progress: 100,
    });
  } catch (error: any) {
    /**
     * 4️⃣ Mark failure
     */
    await Job.findByIdAndUpdate(job._id, {
      status: "FAILED",
      error: error?.message || "Job execution failed",
    });
  }
};
