import { Router } from "express";

import { listJudgments } from "../controllers/judgmentList.controller";
import { getJudgmentById } from "../controllers/judgmentDetail.controller";

import { uploadSingleJudgment } from "../controllers/judgmentUpload.controller";
import { uploadBulkFromInbox } from "../controllers/judgmentBulk.controller";
import { dryRunScan } from "../controllers/judgmentBulk.dryrun";
import { retryNLP } from "../controllers/judgmentRetry.controller";

import { uploadSingleJudgmentPDF } from "../middleware/uploadSingleJudgmentPDF";
import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";

const router = Router();

/**
 * =====================================================
 * 🔓 PUBLIC READ APIs (NO AUTH)
 * =====================================================
 */

/** 📖 List judgments (paginated) */
router.get("/", listJudgments);

/** 📄 Get single judgment by ID */
router.get("/:id", getJudgmentById);

/**
 * =====================================================
 * 🔒 ADMIN / SUPERADMIN ONLY
 * =====================================================
 */

/** ⬆️ Single judgment upload */
router.post(
  "/upload-single",
  auth,
  requireRole(["admin", "superadmin"]),
  uploadSingleJudgmentPDF,
  uploadSingleJudgment
);

/** 📦 Bulk inbox upload */
router.post(
  "/upload-bulk",
  auth,
  requireRole(["admin", "superadmin"]),
  uploadBulkFromInbox
);

/** 🧪 Dry-run inbox scan (no DB write) */
router.get(
  "/upload-dry-run",
  auth,
  requireRole(["admin", "superadmin"]),
  dryRunScan
);

/** 🔁 Retry NLP processing */
router.post(
  "/:judgmentId/retry-nlp",
  auth,
  requireRole(["admin", "superadmin"]),
  retryNLP
);

export default router;
