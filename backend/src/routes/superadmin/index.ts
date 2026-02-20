import { Router } from "express";
import { authenticateJWT } from "../../middlewares/auth.middleware";
import { requireRole } from "../../middlewares/requireRole.middleware";

import { listIngestions } from "../../controllers/superadmin/ingestionList.controller";
import { reprocessIngestion } from "../../controllers/superadmin/reprocessIngestion.controller";

import usersRoutes from "./users.routes";
import uploadRoutes from "./upload.routes";
import uploadAuditRoutes from "./uploadAudit.routes";

const router = Router();

/**
 * Apply authentication + role protection
 * Everything under /superadmin requires superadmin
 */
router.use(authenticateJWT);
router.use(requireRole("superadmin"));

/**
 * Ingestion Monitoring
 */
router.get("/ingestions", listIngestions);

/**
 * Manual reprocess for PERMANENT_FAILURE
 */
router.post("/ingestions/:id/reprocess", reprocessIngestion);

/**
 * Other superadmin modules
 */
router.use("/users", usersRoutes);
router.use("/uploads", uploadRoutes);
router.use("/uploads/audit", uploadAuditRoutes);

export default router;
