import { auth } from "../middlewares/auth.middleware";
import { requireRole } from "../middlewares/role.middleware";

import { Router } from "express";
import { getIngestionStats } from "../controllers/admin/ingestionStats.controller";
import { getSystemHealth } from "../controllers/admin/systemHealth.controller";

const router = Router();

router.get("/ingestion-stats", getIngestionStats);
router.get("/system-health", getSystemHealth);

import { getSystemResources } from "../controllers/admin/systemResources.controller";

router.get(
  "/system-resources",
  auth,
  requireRole("superadmin"),
  getSystemResources
);

export default router;
