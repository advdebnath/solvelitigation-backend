import { Router } from "express";

import { login } from "../controllers/auth/login.controller";
import { logout } from "../controllers/auth/logout.controller";
import { me } from "../controllers/auth/me.controller";

import { authenticateJWT } from "@/middlewares";

const router = Router();

router.post("/login", login);
router.post("/logout", logout);

// 🔐 protected route
router.get("/me", authenticateJWT, me);

export default router;
