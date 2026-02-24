import { Router } from "express";
import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";
import { uploadMiddleware } from "../config/multer";

import {
  enqueueIngestion,
  retryIngestion,
} from "../controllers/ingestion/ingestionControl.controller";

import { uploadJudgmentFolder } from "../controllers/judgmentFolderUpload.controller";
import { getIngestionProgress } from "../controllers/ingestion/ingestionProgress.controller";


const router = Router();

/**
 * ============================================
 * 🔒 SUPERADMIN ONLY
 * ============================================
 */

router.post(
  "/upload-folder",
  auth,
  requireRole(["superadmin"]),
  uploadMiddleware.array("files"),
  uploadJudgmentFolder
);

router.post(
  "/enqueue/:id",
  auth,
  requireRole(["superadmin"]),
  enqueueIngestion
);

router.post(
  "/retry/:id",
  auth,
  requireRole(["superadmin"]),
  retryIngestion
);

router.get(
  "/progress/:id",
  auth,
  requireRole(["superadmin"]),
  getIngestionProgress
);

export default router;
