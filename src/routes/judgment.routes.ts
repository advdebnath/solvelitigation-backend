import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { uploadSingleJudgmentPDF } from "@/middlewares/upload.middleware";
import { uploadSingleJudgment } from "@/controllers/judgmentUpload.controller";

const router = Router();

/**
 * POST /api/judgments/upload-single
 */
router.post(
  "/upload-single",
  authenticateJWT,          // ✅ correct middleware
  uploadSingleJudgmentPDF,
  uploadSingleJudgment
);

export default router;
