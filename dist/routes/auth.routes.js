"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const express_rate_limit_1 = __importDefault(require("express-rate-limit"));
const login_controller_1 = require("../controllers/auth/login.controller");
const me_controller_1 = __importDefault(require("../controllers/auth/me.controller"));
const logout_controller_1 = __importDefault(require("../controllers/auth/logout.controller"));
const auth_middleware_1 = require("../middlewares/auth.middleware");
const router = express_1.default.Router();
const loginLimiter = (0, express_rate_limit_1.default)({
    windowMs: 15 * 60 * 1000,
    max: 10,
});
router.post("/login", loginLimiter, login_controller_1.login);
router.get("/me", auth_middleware_1.authenticateJWT, me_controller_1.default);
router.post("/logout", auth_middleware_1.authenticateJWTOptional, logout_controller_1.default);
exports.default = router;
