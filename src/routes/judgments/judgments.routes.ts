import { Router } from "express";

import { listJudgments } from "@/controllers/judgments/judgments.controller";
import {
  getJudgmentsByCourtType,
  downloadJudgment,
  getUploadStats,
} from "@/controllers/judgments/upload.controller";

import { authenticateJWT } from "@/middlewares/auth.middleware";
import { enforcePlanLimit } from "@/middlewares/planLimit.middleware";

const router = Router();

/**
 * ⚠️ IMPORTANT
 * Legacy judgment upload routes are DISABLED.
 * All uploads MUST go through:
 * POST /api/superadmin/judgments/upload
 */

/* ===================== LIST (PLAN LIMITED) ===================== */

router.get(
  "/",
  authenticateJWT,
  enforcePlanLimit("judgmentsViewed"),
  listJudgments
);

/* ===================== LIST BY COURT (PLAN LIMITED) ===================== */

router.get(
  "/list/:court",
  authenticateJWT,
  enforcePlanLimit("judgmentsViewed"),
  getJudgmentsByCourtType
);

/* ===================== DOWNLOAD (PLAN LIMITED) ===================== */

router.get(
  "/download/:court/:filename",
  authenticateJWT,
  enforcePlanLimit("downloads"),
  downloadJudgment
);

/* ===================== STATS ===================== */

router.get(
  "/stats/all",
  authenticateJWT,
  getUploadStats
);

export default router;
