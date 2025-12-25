import express from "express";
import rateLimit from "express-rate-limit";

import { login } from "@/controllers/auth/login.controller";
import getMe from "@/controllers/auth/me.controller";
import logout from "@/controllers/auth/logout.controller";

import { authenticateJWT, authenticateJWTOptional } from "@/middlewares/auth.middleware";

const router = express.Router();

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
});

router.post("/login", loginLimiter, login);
router.get("/me", authenticateJWT, getMe);
router.post("/logout", authenticateJWTOptional, logout);

export default router;
