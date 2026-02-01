import { Router } from "express";
import { enqueueNlpJobController } from "../controllers/nlp/nlp.enqueue.controller";
import { retryNlpJob } from "../controllers/nlp/nlp.retry.controller";
import { nlpCallback } from "../controllers/nlpCallback.controller";

const router = Router();

// Backend → NLP
router.post("/enqueue", enqueueNlpJobController);

// NLP → Backend callback
router.post("/callback", nlpCallback);

// Manual retry
router.post("/retry/:judgmentId", retryNlpJob);

export default router;
