import { Request, Response } from "express";
import { Types } from "mongoose";
import { Job } from "@/models/job.model";

export const getJobProgress = async (req: Request, res: Response) => {
  try {
    const { jobId } = req.params;
    const user = req.user as any;

    if (!Types.ObjectId.isValid(jobId)) {
      return res.status(400).json({
        success: false,
        message: "Invalid job id",
      });
    }

    const job = await Job.findById(jobId).select(
      "status progress error createdAt updatedAt createdBy totalTasks completedTasks"
    );

    if (!job) {
      return res.status(404).json({
        success: false,
        message: "Job not found",
      });
    }

    const isOwner =
      job.createdBy?.toString() === user.userId ||
      user.role === "superadmin";

    if (!isOwner) {
      return res.status(403).json({
        success: false,
        message: "Access denied",
      });
    }

    return res.json({
      success: true,
      data: {
        status: job.status,
        progress: job.progress ?? 0,
        totalTasks: job.totalTasks ?? null,
        completedTasks: job.completedTasks ?? null,
        error: job.error ?? null,
        createdAt: job.createdAt,
        updatedAt: job.updatedAt,
      },
    });
  } catch (error) {
    console.error("[JOB_PROGRESS_ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch job progress",
    });
  }
};
