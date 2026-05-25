import { Router } from "express";

import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";
import { checkPermission } from "../middleware/permission.middleware";
import { requireCourtAccess } from "../middleware/courtRbac.middleware";
import { COURT_PERMISSIONS } from "../constants/courtPermissions";


import { listJudgments } from "../controllers/judgmentList.controller";
import { getJudgmentById } from "../controllers/judgmentDetail.controller";
import { retryNLP } from "../controllers/judgmentRetry.controller";
import { enqueueJudgmentNlp } from "../controllers/judgmentEnqueue.controller";
import { downloadJudgmentPdf } from "../controllers/judgmentDownload.controller";
import { getJudgmentFilters } from "../controllers/judgmentFilters.controller";
import { reviewJudgment, approveJudgment } from "../controllers/judgment.controller";

import Judgment from "../models/judgment.model";

const router = Router();

/**
 * =====================================================
 * 📄 PUBLIC VIEW (FOR VIEWER)
 * =====================================================
 */
router.get("/view/:id", async (req, res) => {
  try {
    const doc: any = await Judgment.findById(req.params.id).lean();

    if (!doc || Array.isArray(doc)) {
      return res.status(404).json({
        success: false,
        message: "Judgment not found",
      });
    }

    return res.json({
      success: true,
      data: {
        caseNumber: doc?.caseNumber || "",
        court: doc?.courtType || "",
        date: doc?.judgmentDate || "",
        html: doc?.html || "",
        text: doc?.fullText || "",
        headnote: doc?.headnote || "",
        pointsOfLaw: doc?.pointsOfLaw || [],
      },
    });

  } catch (err) {
    console.error("View Judgment Error:", err);

    return res.status(500).json({
      success: false,
      message: "Failed to load judgment",
    });
  }
});

/**
 * =====================================================
 * 📊 FILTER METADATA (AUTH REQUIRED)
 * =====================================================
 */
router.get("/filters", getJudgmentFilters);

/**
 * =====================================================
 * 🔐 AUTHENTICATED READ APIs
 * =====================================================
 */
router.get("/", listJudgments);
router.get("/:id", auth, getJudgmentById);
router.get("/:id/download", auth, downloadJudgmentPdf);

/**
 * =====================================================
 * 🔒 SUPERADMIN ONLY ACTIONS
 * =====================================================
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

router.post(
  "/:judgmentId/retry-nlp",
  auth,
  requireRole(["superadmin"]),
  retryNLP
);

router.post(
  "/:judgmentId/enqueue-nlp",
  auth,
  requireRole(["superadmin"]),
  enqueueJudgmentNlp
);

/**
 * =====================================================
 * 🔐 RBAC ROUTES
 * =====================================================
 */
router.put(
  "/review/:id",
  auth,
  checkPermission(["legal_analyst", "superadmin"]),
  requireCourtAccess([
    "SUPREME",
    "HIGH",
    "TRIBUNAL"
  ]),
  reviewJudgment
);

router.put(
  "/approve/:id",
  auth,
  checkPermission(["editor", "superadmin"]),
  requireCourtAccess([
    "SUPREME",
    "HIGH",
    "TRIBUNAL"
  ]),
  approveJudgment
);

export default router;
