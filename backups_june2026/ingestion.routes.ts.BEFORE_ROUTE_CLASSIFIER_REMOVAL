import { Router, Request, Response, NextFunction } from "express";
import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";
import { upload } from "../middleware/upload.middleware";
import { internalAuth } from "../middleware/internalAuth";

import JudgmentIngestion from "../models/JudgmentIngestion";

import {
  enqueueIngestion,
  retryIngestion,
} from "../controllers/ingestion/ingestionControl.controller";

import { uploadJudgmentFolder } from "../controllers/judgmentFolderUpload.controller";
import { getIngestionProgress } from "../controllers/ingestion/ingestionProgress.controller";

const router = Router();

// ============================================
// 🔥 DOCUMENT TYPE DETECTION ENGINE
// ============================================

const detectDocumentType = (filename: string): string => {
  const name = filename.toLowerCase();

  if (name.includes("rule")) return "RULE";
  if (name.includes("notification")) return "NOTIFICATION";
  if (name.includes("circular")) return "CIRCULAR";
  if (name.includes("act")) return "ACT";

  return "JUDGMENT";
};

// ============================================
// 🔥 MIDDLEWARE → ATTACH DOCUMENT TYPE
// ============================================

const attachDocumentType = (
  req: Request,
  _res: Response,
  next: NextFunction
) => {
  try {
    const files = req.files as Express.Multer.File[];

    if (!files || files.length === 0) return next();

    (req as any).fileMeta = files.map((file) => ({
      originalName: file.originalname,
      documentType: detectDocumentType(file.originalname),
    }));

    console.log("📂 Upload Classification:");
    (req as any).fileMeta.forEach((f: any) => {
      console.log(`➡ ${f.originalName} → ${f.documentType}`);
    });

    next();
  } catch (err) {
    console.error("❌ DocumentType middleware error:", err);
    next();
  }
};

// ============================================
// 🧪 DEBUG ROUTE (NO AUTH)
// ============================================

router.post(
  "/upload-folder-test",
  upload.array("files", 100),
  attachDocumentType,
  uploadJudgmentFolder
);

// ============================================
// 🔐 ADMIN + SUPERADMIN UPLOAD (FINAL FIX)
// ============================================

router.post(
  "/upload-folder",
  auth,
  requireRole(["admin", "superadmin"]), // ✅ upgraded
  upload.array("files", 100),
  attachDocumentType,
  uploadJudgmentFolder
);

// ============================================
// 🔑 INTERNAL SYSTEM UPLOAD (CRITICAL ADD)
// ============================================

router.post(
  "/internal/upload-folder",
  internalAuth,
  upload.array("files", 100),
  attachDocumentType,
  uploadJudgmentFolder
);

// ============================================
// 🔥 ENQUEUE / RETRY
// ============================================

router.post(
  "/enqueue/:id",
  auth,
  requireRole(["admin", "superadmin"]),
  enqueueIngestion
);

router.post(
  "/retry/:id",
  auth,
  requireRole(["admin", "superadmin"]),
  retryIngestion
);

// ============================================
// 🔥 PROGRESS
// ============================================

router.get(
  "/progress/:id",
  auth,
  requireRole(["admin", "superadmin"]),
  getIngestionProgress
);

// ============================================
// 🔥 LIST API (FIXED)
// ============================================

router.get(
  "/list",
  auth,
  requireRole(["admin", "superadmin"]),
  async (_req, res) => {
    try {
      const data = await JudgmentIngestion.find()
        .sort({ createdAt: -1 })
        .limit(100)
        .lean();

      const formatted = data.map((d: any) => ({
        id: d._id,

        fileName:
          d.file?.originalName ||
          d.fileName ||
          "Unknown",

        documentType: d.documentType || "JUDGMENT",

        status: d.status || "UNKNOWN",

        progress:
          d.status === "COMPLETED"
            ? 100
            : d.progress || 0,

        error: d.error || null,
        createdAt: d.createdAt || null,
      }));

      res.json({
        success: true,
        data: formatted,
      });
    } catch (err) {
      console.error("❌ List fetch error:", err);
      res.status(500).json({
        success: false,
        message: "Failed to fetch ingestion list",
      });
    }
  }
);

// ============================================
// 🔥 QUEUE COUNT
// ============================================

router.get(
  "/queue",
  auth,
  requireRole(["admin", "superadmin"]),
  async (_req, res) => {
    try {
      const count = await JudgmentIngestion.countDocuments({
        status: "QUEUED",
      });

      res.json({ success: true, count });
    } catch (err) {
      console.error("❌ Queue count error:", err);
      res.status(500).json({ success: false });
    }
  }
);

export default router;
