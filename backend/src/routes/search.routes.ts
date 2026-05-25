import { Router } from "express";
import { searchJudgments } from "../controllers/search.controller";

const router = Router();

// 🔥 CLEAN ROUTE (NO LOGIC HERE)
router.get("/", searchJudgments);

export default router;
