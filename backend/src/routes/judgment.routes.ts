import { Router } from "express";

import { listJudgments } from "../controllers/judgmentList.controller";
import { getJudgmentById } from "../controllers/judgmentDetail.controller";
import { retryNLP } from "../controllers/judgmentRetry.controller";

import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";

const router = Router();

/**
 * =====================================================
 * 🔓 PUBLIC READ APIs (NO AUTH)
 * =====================================================
 */
router.get("/", listJudgments);
router.get("/:id", getJudgmentById);

/**
 * =====================================================
 * 🔒 ADMIN / SUPERADMIN ONLY
 * =====================================================
 */

/**
 * ⛔ DEPRECATED: single judgment upload
 * This route is intentionally blocked.
 * Use folder ingestion instead.
 */
router.post(
  "/upload-single",
  auth,
  requireRole(["admin", "superadmin"]),
  (_req, res) => {
    return res.status(410).json({
      success: false,
      message:
        "upload-single is deprecated. Use folder upload (ingestion pipeline).",
    });
  }
);

/**
 * 🔁 Retry NLP processing (VALID)
 */
router.post(
  "/:judgmentId/retry-nlp",
  auth,
  requireRole(["admin", "superadmin"]),
  retryNLP
);

import { enqueueJudgmentNlp } from "../controllers/judgmentEnqueue.controller";
router.post("/:judgmentId/enqueue-nlp", enqueueJudgmentNlp);

export default router;
