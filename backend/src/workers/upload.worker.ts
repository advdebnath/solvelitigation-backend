import { Job } from "@/models/job.model";
import { UploadAudit } from "@/models/uploadAudit.model";

export const processUploadJob = async (jobId: string) => {
  const job = await Job.findById(jobId);

  if (!job) {
    throw new Error("Job not found");
  }

  await Job.findByIdAndUpdate(jobId, {
    status: "PROCESSING",
    progress: 0,
  });

  const audit = await UploadAudit.findOne({ jobId });

  if (!audit) {
    throw new Error("Upload audit not found");
  }

  // Each UploadAudit = one file
  const total = 1;

  await Job.findByIdAndUpdate(jobId, {
    totalTasks: total,
    completedTasks: 0,
  });

  await new Promise((r) => setTimeout(r, 300));

  await Job.findByIdAndUpdate(jobId, {
    completedTasks: 1,
    progress: 100,
    status: "COMPLETED",
  });
};
