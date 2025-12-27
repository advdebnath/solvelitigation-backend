import { Request, Response } from "express";
import { UploadAudit } from "@/models/uploadAudit.model";

export const listUploadAudits = async (req: Request, res: Response) => {
  try {
    const page = Math.max(parseInt(req.query.page as string) || 1, 1);
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const skip = (page - 1) * limit;

    const [data, total] = await Promise.all([
      UploadAudit.find()
        .populate("uploadedBy", "name email role")
        .populate("jobId", "status progress error")
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit),
      UploadAudit.countDocuments(),
    ]);

    return res.json({
      success: true,
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
      data,
    });
  } catch (error) {
    console.error("[UPLOAD_AUDIT_LIST_ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch upload audits",
    });
  }
};
