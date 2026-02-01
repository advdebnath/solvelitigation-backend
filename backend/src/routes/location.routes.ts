import { Router } from "express";
import { getStates, getDistricts } from "../controllers/location.controller";

const router = Router();

/**
 * Location routes
 * Base path: /api/location
 */
router.get("/states", getStates);
router.get("/districts/:state", getDistricts);

export default router;
