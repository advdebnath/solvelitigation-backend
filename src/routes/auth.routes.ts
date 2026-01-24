import { Router } from "express";
import { authenticateJWT } from "@/middlewares/auth.middleware";

import { login } from "@/controllers/auth/login.controller";
import { register } from "@/controllers/auth/register.controller";
import { getMe } from "@/controllers/auth/me.controller";
import { logout } from "@/controllers/auth/logout.controller";

const router = Router();

/**
 * Public routes
 */
router.post("/login", login);
router.post("/register", register);

/**
 * Protected routes
 */
router.get("/me", authenticateJWT, getMe);
router.post("/logout", authenticateJWT, logout);

export default router;
