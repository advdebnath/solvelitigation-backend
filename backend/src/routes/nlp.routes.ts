import { Router } from "express";
import { nlpCallbackController } from "../controllers/nlp/nlp.callback.controller";

const router = Router();

// ⚠️ NO AUTH — NLP service is internal
router.post("/callback", nlpCallbackController);

export default router;
