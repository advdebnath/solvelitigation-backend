import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";
import { getMe } from "@/controllers/auth/me.controller";

const router = Router();

router.get("/me", authenticateJWT, getMe);

export default router;
