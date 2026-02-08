import { Router } from "express";
import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";
import { uploadJudgmentFolder } from "../controllers/judgmentFolderUpload.controller";
import { uploadFolder } from "../middleware/uploadFolder.middleware"; // ✅ REQUIRED

const router = Router();

/**
 * 📁 REAL judgment folder upload (INGESTION ONLY)
 * Expected folder structure:
 * YEAR / MONTH / DATE / *.pdf
 */
router.post(
  "/upload-folder",
  auth,
  requireRole(["superadmin"]),
  uploadFolder,               // 🔥 THIS WAS MISSING
  uploadJudgmentFolder
);

export default router;
