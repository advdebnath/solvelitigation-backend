import { Router, Request, Response } from "express";
import { upload900MB } from "../../middlewares/upload.middleware";

const router = Router();

/**
 * POST /api/superadmin/judgments/upload
 * Superadmin PDF upload (single file)
 */
router.post(
  "/judgments/upload",
  upload900MB.single("file"),
  async (req: Request, res: Response) => {
    try {
      if (!req.currentUser) {
        return res.status(401).json({ message: "Unauthorized" });
      }

      return res.status(200).json({
        success: true,
        fileReceived: req.file?.originalname || null,
        size: req.file?.size || 0,
        uploadedBy: req.currentUser._id,
      });
    } catch (err) {
      console.error("Upload error:", err);
      return res.status(500).json({ message: "Upload failed" });
    }
  }
);

export default router;
