import { Router } from "express";

const router = Router();

// ✅ ROOT route (IMPORTANT FIX)
router.get("/", (_req, res) => {
  res.status(200).json({
    success: true,
    service: "solvelitigation-backend",
    status: "ok",
    timestamp: new Date().toISOString(),
  });
});

// ✅ OPTIONAL direct alias (extra safety)
router.get("/ping", (_req, res) => {
  res.status(200).json({
    success: true,
    message: "pong",
    timestamp: new Date().toISOString(),
  });
});

export default router;
