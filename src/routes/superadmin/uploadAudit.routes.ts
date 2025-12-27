import { Router } from "express";
import { listUploadAudits } from "@/controllers/superadmin/uploadAudit.list.controller";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { requireSuperAdmin } from "@/middlewares/requireSuperAdmin";

const router = Router();

/**
 * GET /api/superadmin/uploads
 */
router.get(
  "/uploads",
  authenticateJWT,
  requireSuperAdmin,
  listUploadAudits
);

export default router;
