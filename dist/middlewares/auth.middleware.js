"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateJWT = authenticateJWT;
exports.authenticateJWTOptional = authenticateJWTOptional;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const config_1 = __importDefault(require("../config"));
function authenticateJWT(req, res, next) {
    try {
        const token = req.cookies?.sl_auth;
        if (!token) {
            return res.status(401).json({
                success: false,
                message: "Authentication required",
            });
        }
        const decoded = jsonwebtoken_1.default.verify(token, config_1.default.jwtSecret);
        if (!decoded?.userId || !decoded?.role) {
            return res.status(401).json({
                success: false,
                message: "Invalid token payload",
            });
        }
        req.user = {
            userId: decoded.userId,
            role: decoded.role,
        };
        next();
    }
    catch {
        return res.status(401).json({
            success: false,
            message: "Invalid or expired token",
        });
    }
}
function authenticateJWTOptional(req, _res, next) {
    try {
        const token = req.cookies?.sl_auth;
        if (!token)
            return next();
        const decoded = jsonwebtoken_1.default.verify(token, config_1.default.jwtSecret);
        if (decoded?.userId && decoded?.role) {
            req.user = {
                userId: decoded.userId,
                role: decoded.role,
            };
        }
    }
    catch {
        // ignore optional auth errors
    }
    next();
}
