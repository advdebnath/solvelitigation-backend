import { Router } from "express";
import { analyzeJudgment } from "@/controllers/nlp/nlp.controller";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { enforcePlanLimit } from "@/middlewares/planLimit.middleware";

const router = Router();

/**
 * POST /api/nlp/analyze
 * 🔐 Auth required
 * 📊 Counts toward AI plan usage
 */
router.post(
  "/analyze",
  authenticateJWT,
  enforcePlanLimit("aiRequests"),
  analyzeJudgment
);

export default router;
