import { getIngestionStats } from "../controllers/admin/ingestion.monitor.controller";
import { getFailedIngestions, retryFailedIngestion } from "../controllers/admin/ingestion.monitor.controller";
import { Router } from "express";

import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";

import { getSystemHealth } from "../controllers/admin/systemHealth.controller";
import { getSystemResources } from "../controllers/admin/systemResources.controller";
import { getSystemStats } from "../controllers/admin/systemStats.controller";

const router = Router();

/* =====================================================
   🔐 SUPERADMIN PROTECTED ROUTES
===================================================== */

/**
 * 📊 Full system stats (production metrics)
 */
router.get(
  "/system-stats",
  auth,
  requireRole(["superadmin"]),
  getSystemStats
);

/**
 * 📦 Ingestion stats breakdown
 */
router.get(
  "/ingestion-stats",
  auth,
  requireRole(["superadmin"]),
  getIngestionStats
);

/**
 * ❤️ System health check (DB + Redis)
 */
router.get(
  "/system-health",
  auth,
  requireRole(["superadmin"]),
  getSystemHealth
);

/**
 * 🖥 System resource usage (CPU / Memory)
 */
router.get(
  "/system-resources",
  auth,
  requireRole(["superadmin"]),
  getSystemResources
);

/**
 * 🔁 Retry all failed ingestions
 */
router.post(
  "/retry-failed",
  auth,
  requireRole(["superadmin"]),
);

router.get("/ingestions/failed", getFailedIngestions);
router.post("/ingestions/retry/:id", retryFailedIngestion);

router.get("/ingestions/stats", getIngestionStats);

export default router;
