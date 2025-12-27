import { Router } from "express";
import { upload900MB } from "@/middlewares/upload.middleware";

const router = Router();

/**
 * POST /api/superadmin/judgments/upload
 * Superadmin PDF upload (900MB per file)
 */
router.post(
  "/upload",
  upload900MB.array("files"),
  (req, res) => {
    return res.json({
      success: true,
      filesReceived: req.files?.length || 0,
    });
  }
);

export default router;
