import {
  enqueueIngestion,
  retryIngestion,
} from "../controllers/ingestion/ingestionControl.controller";

import { Router } from "express";
import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";
import { uploadMiddleware } from "../config/multer";

import { uploadJudgmentFolder } from "../controllers/judgmentFolderUpload.controller";
import { getIngestionProgress } from "../controllers/ingestion/ingestionProgress.controller";

const router = Router();

/**
 * Folder upload (superadmin only)
 */
router.post(
  "/upload-folder",
  auth,
  requireRole(["superadmin"]),
  uploadMiddleware.array("files"),
  uploadJudgmentFolder
);

/**
 * Ingestion progress (superadmin)
 */
router.get(
  "/progress",
  auth,
  requireRole(["superadmin"]),
  getIngestionProgress
);

/**
 * Manual enqueue (superadmin)
 */
router.post(
  "/:id/enqueue",
  auth,
  requireRole(["superadmin"]),
  enqueueIngestion
);

/**
 * Retry failed ingestion (superadmin)
 */
router.post(
  "/:id/retry",
  auth,
  requireRole(["superadmin"]),
  retryIngestion
);

export default router;
