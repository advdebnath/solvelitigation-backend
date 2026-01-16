import { Router } from "express";
import { getStates, getDistricts } from "@/controllers/location.controller";

const router = Router();

router.get("/states", getStates);
router.get("/districts/:state", getDistricts);

export default router;
