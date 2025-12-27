import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { uploadJudgments } from "@/controllers/superadmin/judgment.upload.controller";
import { requireSuperAdmin } from "@/middlewares/requireSuperAdmin";
import { uploadFolder } from "@/middlewares/uploadFolder.middleware";

const router = Router();

/**
 * PRIMARY upload endpoint
 */
router.post(
  "/upload",
  authenticateJWT,
  requireSuperAdmin,
  uploadFolder,
  uploadJudgments
);

/**
 * BACKWARD-COMPATIBILITY ALIASES
 */
router.post(
  "/supreme/upload-folder",
  authenticateJWT,
  requireSuperAdmin,
  uploadFolder,
  uploadJudgments
);

router.post(
  "/high/upload-folder",
  authenticateJWT,
  requireSuperAdmin,
  uploadFolder,
  uploadJudgments
);

router.post(
  "/tribunal/upload-folder",
  authenticateJWT,
  requireSuperAdmin,
  uploadFolder,
  uploadJudgments
);

export default router;
