import { Router } from "express";

import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";

import { listJudgments } from "../controllers/judgmentList.controller";
import { getJudgmentById } from "../controllers/judgmentDetail.controller";
import { retryNLP } from "../controllers/judgmentRetry.controller";
import { enqueueJudgmentNlp } from "../controllers/judgmentEnqueue.controller";
import { downloadJudgmentPdf } from "../controllers/judgmentDownload.controller";
import { getJudgmentFilters } from "../controllers/judgmentFilters.controller";

const router = Router();

/**
 * =====================================================
 * 📊 FILTER METADATA (AUTH REQUIRED)
 * =====================================================
 */
router.get("/filters", auth, getJudgmentFilters);

/**
 * =====================================================
 * 🔐 AUTHENTICATED READ APIs
 * Logged-in users can browse, view and download judgments
 * =====================================================
 */
router.get("/", auth, listJudgments);
router.get("/:id", auth, getJudgmentById);
router.get("/:id/download", auth, downloadJudgmentPdf);

/**
 * =====================================================
 * 🔒 SUPERADMIN ONLY ACTIONS
 * =====================================================
 */

/**
 * ⛔ Deprecated single upload
 */
router.post(
  "/upload-single",
  auth,
  requireRole(["superadmin"]),
  (_req, res) => {
    return res.status(410).json({
      success: false,
      message:
        "upload-single is deprecated. Use folder upload (ingestion pipeline).",
    });
  }
);

/**
 * 🔁 Retry NLP
 */
router.post(
  "/:judgmentId/retry-nlp",
  auth,
  requireRole(["superadmin"]),
  retryNLP
);

/**
 * 🚀 Manual enqueue NLP
 */
router.post(
  "/:judgmentId/enqueue-nlp",
  auth,
  requireRole(["superadmin"]),
  enqueueJudgmentNlp
);

export default router;
