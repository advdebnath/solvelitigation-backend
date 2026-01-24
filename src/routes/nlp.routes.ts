import { Router } from "express";
import {
  nlpHealthCheck,
  analyzeJudgment,
} from "@/controllers/nlp.controller";
import { authenticateJWT } from "@/middlewares/auth.middleware";

const router = Router();

router.get("/health", nlpHealthCheck);
router.post("/analyze", authenticateJWT, analyzeJudgment);

export default router;
