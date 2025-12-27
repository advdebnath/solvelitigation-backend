import { Router } from "express";
import uploadRoutes from "./upload.routes";

const router = Router();

/**
 * /api/superadmin/judgments/upload
 */
router.use("/judgments", uploadRoutes);

import uploadAuditRoutes from "./uploadAudit.routes";
router.use(uploadAuditRoutes);

export default router;
