import { Router } from "express";
import { listJudgments } from "@/controllers/judgments/judgments.controller";
import { authenticateJWT } from "@/middlewares/auth.middleware";

const router = Router();

// Paid users only
router.get("/", authenticateJWT, listJudgments);

export default router;
