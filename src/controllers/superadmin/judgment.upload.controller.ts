import { Job } from "@/models/job.model";
import { Request, Response } from "express";
import { UploadAudit } from "@/models/uploadAudit.model";
import { enqueueJob } from "@/services/job.service";

export const uploadJudgments = async (req: Request, res: Response) => {
  try {
    const user = req.user as any;

    const files = (req.files as Express.Multer.File[]) || [];
    const filesCount = files.length;

    const courtType =
      req.path.includes("supreme")
        ? "SUPREME"
        : req.path.includes("high")
        ? "HIGH"
        : "TRIBUNAL";

    /**
     * 1️⃣ Create upload audit
     */
    const audit = await UploadAudit.create({
      uploadedBy: user.userId,
      role: user.role,
      courtType,
      filesCount,
      status: "PROCESSING",
    });

    /**
     * 2️⃣ Enqueue job
     */
    const job = await enqueueJob({
      type: "UPLOAD_JUDGMENTS",
      payload: {
        auditId: audit._id,
        courtType,
        uploadedBy: user.userId.toString(),
      },
    });

    /**
     * 3️⃣ Ensure job status is PROCESSING
     */
    await Job.findByIdAndUpdate(job._id, { status: "PROCESSING" });

    /**
     * 4️⃣ Link audit ↔ job
     */
    audit.jobId = job._id;
    await audit.save();

    return res.status(202).json({
      success: true,
      message: "Upload registered and queued for processing",
      auditId: audit._id,
      jobId: job._id,
    });
  } catch (error) {
    console.error("[UPLOAD_JUDGMENTS_ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Failed to register upload",
    });
  }
};
