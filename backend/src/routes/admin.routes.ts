import { Router } from "express";
import { getIngestionStats } from "../controllers/admin/ingestionStats.controller";
import { getSystemHealth } from "../controllers/admin/systemHealth.controller";

const router = Router();

router.get("/ingestion-stats", getIngestionStats);
router.get("/system-health", getSystemHealth);

export default router;
