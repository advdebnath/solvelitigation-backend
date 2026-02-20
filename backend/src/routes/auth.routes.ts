import { Router } from "express";

import { login } from "../controllers/auth/login.controller";
import { logout } from "../controllers/auth/logout.controller";
import { me } from "../controllers/auth/me.controller";
import { register } from "../controllers/auth/register.controller";

import { authenticateJWT } from "../middlewares/auth.middleware";
import { authLimiter } from "../middlewares/rateLimit.middleware"; // 👈 add this

const router = Router();

router.post("/register", register);

// 🔐 Apply limiter ONLY to login
router.post("/login", authLimiter, login);

router.post("/logout", logout);

// 🔐 protected route
router.get("/me", authenticateJWT, me);

export default router;
