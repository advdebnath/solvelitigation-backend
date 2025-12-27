import { Router } from "express";
import { getJobProgress } from "@/controllers/job/job.progress.controller";
import { authenticateJWT } from "@/middlewares/auth.middleware";

const router = Router();

/**
 * GET /api/jobs/:jobId/progress
 */
router.get(
  "/:jobId/progress",
  authenticateJWT,
  getJobProgress
);

export default router;
