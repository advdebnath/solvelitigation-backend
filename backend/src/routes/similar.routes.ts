import { Router } from "express";
import { getSimilarCases } from "../controllers/similar.controller";

const router = Router();

// 👉 API
router.get("/:id", getSimilarCases);

export default router;
