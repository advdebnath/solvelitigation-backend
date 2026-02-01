import { Router } from "express";
import { nlpCallback } from "../controllers/nlpCallback.controller";

const router = Router();

// NLP → Backend callback
router.post("/callback", nlpCallback);

export default router;



