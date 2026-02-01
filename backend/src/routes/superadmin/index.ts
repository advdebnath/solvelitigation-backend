import { Router } from "express";
import { authenticateJWT } from "../../middlewares/auth.middleware";
import { requireRole } from "../../middlewares/requireRole.middleware";

import usersRoutes from "./users.routes";
import uploadRoutes from "./upload.routes";
import uploadAuditRoutes from "./uploadAudit.routes";

const router = Router();

router.use(authenticateJWT);
router.use(requireRole("superadmin"));

router.use("/users", usersRoutes);
router.use("/uploads", uploadRoutes);
router.use("/uploads/audit", uploadAuditRoutes);

export default router;
