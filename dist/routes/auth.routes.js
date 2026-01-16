"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const auth_middleware_1 = require("../middlewares/auth.middleware");
const me_controller_1 = require("../controllers/auth/me.controller");
const router = (0, express_1.Router)();
router.get("/me", auth_middleware_1.authenticateJWT, me_controller_1.getMe);
exports.default = router;
