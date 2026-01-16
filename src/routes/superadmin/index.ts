import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { requireRole } from "@/middlewares/role.middleware";
import uploadAuditRoutes from "./uploadAudit.routes";
import judgmentUploadRoutes from "./judgment.upload.routes";

const router = Router();

/**
 * 🔐 GLOBAL PROTECTION
 * Applies to ALL /api/superadmin/* routes
 */
router.use(authenticateJWT, requireRole(["superadmin"]));

/**
 * /api/superadmin/judgments/upload
 * Mount judgment upload routes
 */
router.use("/judgments", judgmentUploadRoutes);

/**
 * /api/superadmin/audits
 * Mount audit routes
 */
router.use("/audits", uploadAuditRoutes);

export default router;
