"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateJWT = authenticateJWT;
exports.requireSuperAdmin = requireSuperAdmin;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const mongoose_1 = __importDefault(require("mongoose"));
const user_model_1 = require("../models/user.model");
const config_1 = __importDefault(require("../config"));
/**
 * Core auth middleware
 */
async function authenticateJWT(req, res, next) {
    try {
        const token = req.cookies?.[config_1.default.AUTH_COOKIE_NAME] ||
            req.headers.authorization?.replace("Bearer ", "");
        if (!token) {
            return res.status(401).json({ message: "Unauthorized" });
        }
        const decoded = jsonwebtoken_1.default.verify(token, config_1.default.jwtSecret);
        if (!mongoose_1.default.Types.ObjectId.isValid(decoded.userId)) {
            return res.status(401).json({ message: "Invalid token" });
        }
        const user = (await user_model_1.User.findOne({
            _id: decoded.userId,
            isDeleted: false,
        }).lean());
        if (!user) {
            return res.status(401).json({ message: "User not found" });
        }
        const normalizedUser = {
            _id: user._id.toString(),
            name: user.name,
            email: user.email,
            role: user.role,
            plan: user.plan,
            planStatus: user.planStatus,
            planExpiresAt: user.planExpiresAt ?? null,
            usage: user.usage ?? {
                downloads: 0,
                aiRequests: 0,
                judgmentsViewed: 0,
            },
            grace: user.grace ?? null,
            isVerified: user.isVerified,
        };
        // ✅ Backward compatibility
        req.user = normalizedUser;
        req.currentUser = normalizedUser;
        next();
    }
    catch {
        return res.status(401).json({ message: "Authentication failed" });
    }
}
/**
 * Superadmin guard
 */
function requireSuperAdmin(req, res, next) {
    const user = req.user || req.currentUser;
    if (!user || user.role !== "superadmin") {
        return res.status(403).json({
            success: false,
            message: "Superadmin access required",
        });
    }
    next();
}
