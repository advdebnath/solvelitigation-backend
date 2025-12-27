import { Router } from "express";
import { getActsByCategory } from "../controllers/act.controller";

const router = Router();

/**
 * @route   GET /api/acts
 * @query   category=civil|criminal|service|tax
 */
router.get("/", getActsByCategory);

export default router;
