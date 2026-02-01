import { Router } from "express";

import { listUploadAudits } from "../../controllers/superadmin/uploadAudit.list.controller";
import { authenticateJWT } from "../../middlewares/auth.middleware";
import { requireSuperadmin } from "../../middlewares/requireSuperadmin";

const router = Router();

/**
 * GET /api/superadmin/uploads
 */
router.get(
  "/uploads",
  authenticateJWT,
  requireSuperadmin,
  listUploadAudits
);

export default router;
