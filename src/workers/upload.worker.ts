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

  const total = audit?.filesCount ?? 1;

  await Job.findByIdAndUpdate(jobId, {
    totalTasks: total,
    completedTasks: 0,
  });

  for (let i = 1; i <= total; i++) {
    // simulate file processing (real logic later)
    await new Promise((r) => setTimeout(r, 300));

    await Job.findByIdAndUpdate(jobId, {
      completedTasks: i,
      progress: Math.round((i / total) * 100),
    });
  }

  await Job.findByIdAndUpdate(jobId, {
    status: "COMPLETED",
    progress: 100,
  });
};
